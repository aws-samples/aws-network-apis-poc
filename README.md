# AWS Network APIs POC

This CDK package will deploy EC2 Instances into an AWS Region and Wavelength Zone.

## Setup

1. Ensure your AWS Account is opted-in for WLZs. You can do this on the EC2 Dashboard page (Zones --> Enable additional Zones).
2. Follow the [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) to setup the AWS CLI and AWS CDK for TypeScript.
3. Update `bin/mec.ts` with your desired configuration (i.e. AZ, WLZ, Key-Pair, CIDR Blocks, AMIs, and Instance Types) and `lib/mec-stack.ts` with the correct Security Group rules for your instances.
4. Build the stack.
```
npm install && npm run build
```
5. Deploy the stack.
```
cdk deploy MecStackDFW
```
6. [Optional] If the CDK is failing due to Subnet and Route Table Associations, delete the stack manually in the CFN console, comment out the occurances of the `ec2.CfnSubnetRouteTableAssociation()` function call, and build/deploy the CFN stack. Once the deployment is complete, recomment those function calls back in and build/deploy the CFN stack.

## Bastion Host Setup
### On the Local Machine
```
# Update your ~/.ssh/config with the following
Host bastionhost
  Hostname [INSERT BASTION HOST PUBLIC IP]
  user ubuntu
  IdentityFile [INSERT PATH TO KEY-PAIR FILE]
  Port 22
  ForwardAgent yes
  ServerAliveInterval 240
  LogLevel DEBUG
  
# [Optional] Clean your ssh-add keys
ssh-add -D
  
# Add the KEY-PAIR to your SSH keys
ssh-add [INSERT PATH TO KEY-PAIR FILE]

# Confirm the KEY-PAIR was added
ssh-add -l

# Connect to the bastion host
ssh bastionhost
```
### On the Bastion Host
```
# Connect to the private EC2 Instances
ssh -v ubuntu@[INSERT EC2 INSTANCE PRIVATE IP]
```

## Useful commands
* `npm install`     download package and it's dependencies
* `npm run build`   compile typescript to js
* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

