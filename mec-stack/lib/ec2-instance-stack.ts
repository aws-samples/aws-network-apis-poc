#!/usr/bin/env node
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export interface Ec2InstanceStackProps extends cdk.StackProps {
  readonly az: string
  readonly keyname: string
  readonly vpcCIDR: string
  readonly publicAZSubnetCIDR: string
  readonly imageId: string
  readonly instanceType: string
}

export class Ec2InstanceStack extends cdk.Stack {
  readonly vpc: ec2.Vpc;
  readonly igw: ec2.CfnInternetGateway;

  constructor(parent: Construct, id: string, props: Ec2InstanceStackProps) {
    super(parent, id, props);
    [this.vpc, this.igw] = this.createVpc(props)
    this.createPublicAZEC2Instance(props, this.vpc, this.igw)
  }

    /**
     * Create a VPC with an IGW.
     */
    private createVpc(props: Ec2InstanceStackProps): [ec2.Vpc, ec2.CfnInternetGateway] {
      // Create the VPC
      const vpc = new ec2.Vpc(this, 'ec2-vpc', {
          availabilityZones: [props.az],
          enableDnsHostnames: false,
          ipAddresses: ec2.IpAddresses.cidr(props.vpcCIDR),
          natGateways: 0,
          subnetConfiguration: [],
          vpcName: 'ec2-vpc',
      });

      // Create the IGW for the VPC
      const igw = new ec2.CfnInternetGateway(this, 'ec2-igw', {
          tags: [{
            key: 'Name',
            value: 'ec2-igw',
          }],
      });

      // Associate the VPC with the IGW
      new ec2.CfnVPCGatewayAttachment(this, 'ec2-vpc-gateway-attachement', {
          vpcId: vpc.vpcId,
          internetGatewayId: igw.attrInternetGatewayId,
      });

      // CFN Outputs
      new cdk.CfnOutput(this, 'vpcId', { value: vpc.vpcId });

      return [vpc, igw]
  }

  /**
   * Create Public AZ EC2 Instance.
   * 
   * NOTE: Security Group Rules are defined inline!
   */
  private createPublicAZEC2Instance(props: Ec2InstanceStackProps, vpc: ec2.Vpc, igw: ec2.CfnInternetGateway) {
      // Create the Public Subnet in an AZ
      const publicAZSubnet = new ec2.Subnet(this, 'ec2-public-az-subnet', {
          availabilityZone: props.az,
          cidrBlock: props.publicAZSubnetCIDR,
          vpcId: vpc.vpcId,
          mapPublicIpOnLaunch: true,
      });

      // Create the Route Table for the Public Subnet in an AZ
      const publicAZSubnetRTB = new ec2.CfnRouteTable(this,  'ec2-public-az-subnet-rtb', {
          vpcId: vpc.vpcId,
          tags: [
              {
                  key: 'Name',
                  value: 'ec2-public-az-subnet-rtb',
              }
          ]
      });

      // Create the Route to the IGW
      new ec2.CfnRoute(this, 'ec2-public-az-subnet-rtb-route', {
          routeTableId: publicAZSubnetRTB.attrRouteTableId,
          gatewayId: igw.attrInternetGatewayId,
          destinationCidrBlock: '0.0.0.0/0',
      });

      // Associate the Route Table with the Public Subnet in an AZ
      new ec2.CfnSubnetRouteTableAssociation(this, 'ec2-public-az-subnet-rtb-association', {
          subnetId: publicAZSubnet.subnetId,
          routeTableId: publicAZSubnetRTB.attrRouteTableId,
      });

      // Create the Security Group for the EC2 Instance
      const sg = new ec2.SecurityGroup(this, 'ec2-sg', {
          vpc: vpc,
          allowAllOutbound: true
      });
      sg.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(22))
      sg.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80))

      // Create the EC2 Instance
      const ec2Instance = new ec2.CfnInstance(this, 'ec2-instance', {
          availabilityZone: publicAZSubnet.availabilityZone,
          imageId: props.imageId,
          instanceType: props.instanceType,
          keyName: props.keyname,
          networkInterfaces: [
              {
                  associatePublicIpAddress: true,
                  deviceIndex: '0',
                  groupSet: [sg.securityGroupId],
                  subnetId: publicAZSubnet.subnetId,
              }
          ],
          tags: [
              {
                  key: 'Name',
                  value: 'ec2',
              }
          ],
      });

      // CFN Outputs        
      new cdk.CfnOutput(this, 'publicAZSubnetId', { value: publicAZSubnet.subnetId });
      new cdk.CfnOutput(this, 'sg', { value: sg.securityGroupId });
      new cdk.CfnOutput(this, 'ec2Instance', { value: ec2Instance.ref });
  }
}
