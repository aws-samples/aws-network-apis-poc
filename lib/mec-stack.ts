#!/usr/bin/env node
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export interface MecStackProps extends cdk.StackProps {
    readonly az: string
    readonly wlz: string
    readonly keyname: string
    readonly vpcCIDR: string
    readonly publicAZSubnetCIDR: string
    readonly publicWLZSubnetCIDR: string
    readonly bastionhostImageId: string
    readonly bastionhostInstanceType: string
    readonly publicWLZInstance1ImageId: string
    readonly publicWLZInstance1Type: string
    readonly publicWLZInstance2ImageId: string
    readonly publicWLZInstance2Type: string
}

export class MecStack extends cdk.Stack {  
    readonly vpc: ec2.Vpc;
    readonly igw: ec2.CfnInternetGateway;
    readonly cgw: ec2.CfnCarrierGateway;

    constructor(parent: Construct, id: string, props: MecStackProps) {
        super(parent, id, props);
        [this.vpc, this.igw, this.cgw] = this.createVpc(props)
        this.createPublicAZEC2Instance(props, this.vpc, this.igw)
        this.createPublicWLZEC2Instances(props, this.vpc, this.cgw)
    }

    /**
     * Create a VPC with an IGW and a CGW.
     */
    private createVpc(props: MecStackProps): [ec2.Vpc, ec2.CfnInternetGateway, ec2.CfnCarrierGateway] {
        // Create the VPC
        const vpc = new ec2.Vpc(this, 'mec-vpc', {
            availabilityZones: [props.az, props.wlz],
            enableDnsHostnames: false,
            ipAddresses: ec2.IpAddresses.cidr(props.vpcCIDR),
            natGateways: 0,
            subnetConfiguration: [],
            vpcName: 'mec-vpc',
        });

        // Create the IGW for the VPC
        const igw = new ec2.CfnInternetGateway(this, 'mec-igw', {
            tags: [{
              key: 'Name',
              value: 'mec-igw',
            }],
        });

        // Associate the VPC with the IGW
        new ec2.CfnVPCGatewayAttachment(this, 'mec-vpc-gateway-attachement', {
            vpcId: vpc.vpcId,
            internetGatewayId: igw.attrInternetGatewayId,
        });

        // Create the CGW for the VPC
        const cgw = new ec2.CfnCarrierGateway(this, 'mec-cgw', {
            vpcId: vpc.vpcId,
            tags: [
                {
                    key: 'Name',
                    value: 'mec-cgw',
                }
            ]
        });

        // CFN Outputs
        new cdk.CfnOutput(this, 'vpcId', { value: vpc.vpcId });

        return [vpc, igw, cgw]
    }

    /**
     * Create Public AZ EC2 Instance.
     * 
     * NOTE: Security Group Rules are defined inline!
     */
    private createPublicAZEC2Instance(props: MecStackProps, vpc: ec2.Vpc, igw: ec2.CfnInternetGateway) {
        // Create the Public Subnet in an AZ
        const publicAZSubnet = new ec2.Subnet(this, 'mec-public-az-subnet', {
            availabilityZone: props.az,
            cidrBlock: props.publicAZSubnetCIDR,
            vpcId: vpc.vpcId,
            mapPublicIpOnLaunch: true,
        });

        // Create the Route Table for the Public Subnet in an AZ
        const publicAZSubnetRTB = new ec2.CfnRouteTable(this,  'mec-public-az-subnet-rtb', {
            vpcId: vpc.vpcId,
            tags: [
                {
                    key: 'Name',
                    value: 'mec-public-az-subnet-rtb',
                }
            ]
        });

        // Create the Route to the IGW
        new ec2.CfnRoute(this, 'mec-public-az-subnet-rtb-route', {
            routeTableId: publicAZSubnetRTB.attrRouteTableId,
            gatewayId: igw.attrInternetGatewayId,
            destinationCidrBlock: '0.0.0.0/0',
        });

        // Associate the Route Table with the Public Subnet in an AZ
        new ec2.CfnSubnetRouteTableAssociation(this, 'mec-public-az-subnet-rtb-association', {
            subnetId: publicAZSubnet.subnetId,
            routeTableId: publicAZSubnetRTB.attrRouteTableId,
        });

        // Create the Security Group for the Bastion Host
        const bastionhostSG = new ec2.SecurityGroup(this, 'mec-bastionhost-sg', {
            vpc: vpc,
            allowAllOutbound: true
        });
        bastionhostSG.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(22))

        // Create the Bastion Host EC2 Instance
        const bastionhostEC2Instance = new ec2.CfnInstance(this, 'mec-bastionhost', {
            availabilityZone: publicAZSubnet.availabilityZone,
            imageId: props.bastionhostImageId,
            instanceType: props.bastionhostInstanceType,
            keyName: props.keyname,
            networkInterfaces: [
                {
                    associatePublicIpAddress: true,
                    deviceIndex: '0',
                    groupSet: [bastionhostSG.securityGroupId],
                    subnetId: publicAZSubnet.subnetId,
                }
            ],
            tags: [
                {
                    key: 'Name',
                    value: 'mec-bastionhost',
                }
            ],
        });

        // CFN Outputs        
        new cdk.CfnOutput(this, 'publicAZSubnetId', { value: publicAZSubnet.subnetId });
        new cdk.CfnOutput(this, 'bastionhostSGId', { value: bastionhostSG.securityGroupId });
        new cdk.CfnOutput(this, 'bastionhostEC2Instance', { value: bastionhostEC2Instance.ref });
    }

    /**
     * Create the Public WLZ ML Model and Video Mixer EC2 Instances.
     * 
     * NOTE: Security Group Rules are defined inline!
     */
    private createPublicWLZEC2Instances(props: MecStackProps, vpc: ec2.Vpc, cgw: ec2.CfnCarrierGateway) {
        // Create the Public Subnet in the WLZ
        const publicWLZSubnet = new ec2.Subnet(this, 'mec-public-wlz-subnet', {
            vpcId: vpc.vpcId,
            availabilityZone: props.wlz,
            cidrBlock: props.publicWLZSubnetCIDR,
        });

        // Create the Route Table for the Public Subnet in an WLZ
        const publicWLZSubnetRTB = new ec2.CfnRouteTable(this,  'mec-public-wlz-subnet-rtb', {
            vpcId: vpc.vpcId,
            tags: [
                {
                    key: 'Name',
                    value: 'mec-public-wlz-subnet-rtb',
                }
            ]
        });

        // Create the Route to the CGW
        new ec2.CfnRoute(this, 'mec-public-wlz-subnet-rtb-route', {
            routeTableId: publicWLZSubnetRTB.attrRouteTableId,
            carrierGatewayId: cgw.attrCarrierGatewayId,
            destinationCidrBlock: '0.0.0.0/0',
        });

        // Associate the Route Table with the Public Subnet in the WLZ
        new ec2.CfnSubnetRouteTableAssociation(this, 'mec-public-wlz-subnet-rtb-association', {
            subnetId: publicWLZSubnet.subnetId,
            routeTableId: publicWLZSubnetRTB.attrRouteTableId,
        });

        // Create the Security Group for EC2 Instance 1
        const EC2InstanceSG_1 = new ec2.SecurityGroup(this, 'mec-ec2-instance-1-sg', {
            vpc: vpc,
            allowAllOutbound: true
        });
        EC2InstanceSG_1.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(22))
        EC2InstanceSG_1.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.udp(1194))
        EC2InstanceSG_1.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80))

        // Create EC2 Instance 1
        const EC2Instance_1 = new ec2.CfnInstance(this, 'mec-ec2-instance-1', {
            availabilityZone: publicWLZSubnet.availabilityZone,
            imageId: props.publicWLZInstance1ImageId,
            instanceType: props.publicWLZInstance1Type,
            keyName: props.keyname,
            networkInterfaces: [
                {
                    associateCarrierIpAddress: true,
                    deviceIndex: '0',
                    groupSet: [EC2InstanceSG_1.securityGroupId],
                    subnetId: publicWLZSubnet.subnetId,
                }
            ],
            tags: [
                {
                    key: 'Name',
                    value: 'mec-ec2-instance-1',
                }
            ],
        });

        // Create the Security Group for EC2 Instance 2
        const EC2InstanceSG_2 = new ec2.SecurityGroup(this, 'mec-ec2-instance-2-sg', {
            vpc: vpc,
            allowAllOutbound: true
        });
        EC2InstanceSG_2.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(22))
        EC2InstanceSG_2.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.udp(1194))
        EC2InstanceSG_2.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80))

        // Create EC2 Instance 2
        const EC2Instance_2 = new ec2.CfnInstance(this, 'mec-ec2-instance-2', {
            availabilityZone: publicWLZSubnet.availabilityZone,
            imageId: props.publicWLZInstance2ImageId,
            instanceType: props.publicWLZInstance2Type,
            keyName: props.keyname,
            networkInterfaces: [
                {
                    associateCarrierIpAddress: true,
                    deviceIndex: '0',
                    groupSet: [EC2InstanceSG_2.securityGroupId],
                    subnetId: publicWLZSubnet.subnetId,
                }
            ],
            tags: [
                {
                    key: 'Name',
                    value: 'mec-ec2-instance-2',
                }
            ],
        });

        // CFN Outputs
        new cdk.CfnOutput(this, 'publicWLZSubnet', { value: publicWLZSubnet.subnetId });
        new cdk.CfnOutput(this, 'EC2InstanceSG_1', { value: EC2InstanceSG_1.securityGroupId });
        new cdk.CfnOutput(this, 'EC2Instance_1', { value: EC2Instance_1.ref });
        new cdk.CfnOutput(this, 'EC2InstanceSG_2', { value: EC2InstanceSG_2.securityGroupId });
        new cdk.CfnOutput(this, 'EC2Instance_2', { value: EC2Instance_2.ref });
    }
}
