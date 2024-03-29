# Developer Kit

This repository is for the Developer Kit.

## Step 1: Deploy a publicly accessible EC2 instance to a Wavelength Zone

In this step, please use the `mec-stack` directory.

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

###  Bastion Host Setup
#### On the Local Machine
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
#### On the Bastion Host
```
# Connect to the private EC2 Instances
ssh -v ubuntu@[INSERT EC2 INSTANCE PRIVATE IP]
```

#### Useful commands
* `npm install`     download package and it's dependencies
* `npm run build`   compile typescript to js
* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template

## Step 2: Deploy an publicly accessible EC2 instance to a Region

In this step, please use the `mec-stack` directory.

1. Follow the [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) to setup the AWS CLI and AWS CDK for TypeScript.
2. Build the stack.
3. Update `bin/mec.ts` with your desired configuration (i.e. AZ, Key-Pair, CIDR Blocks, AMIs, and Instance Types) and `lib/ec2-instance-stack.ts` with the correct Security Group rules for your instances.
```
npm install && npm run build
```
4. Deploy the stack.
```
cdk deploy EC2InstanceStack
```

## Step 3: Run a JWKS Server on the EC2 instance in the Region

In this step, please use the `jwks-server` directory.

1. Use https://mkjwk.org/ to create your JWK (JSON Web Key).
2. Use https://8gwifi.org/jwkconvertfunctions.jsp to convert your JWK into a RSA PEM encoded public and private key.
3. SSH into the EC2 instance your provisioned in Step 2.
4. Clone the `jwks-server` directory onto the EC2 instance.
5. Update the public key with the public key from the JWK you created in Step 3.1.
6. Run the Flask Server. You can either execute `make python` to run the Flask App using Python, or execute `make build` to build the Flask App in a Docker Container and then `make run` to launch the Docker Container.

## Step 4: Run the Developer Kit

In this step, please use the `developer-kit` directory.

1. Update the `.env` with your specific configuration. Note that the private key must be the matching private key for the public key you created in Step 3.2.
2. Run the Flask Server. You can either execute `make python` to run the Flask App using Python, or execute `make build` to build the Flask App in a Docker Container and then `make run` to launch the Docker Container.
3. Update the files in the `config` directory and then begin interacting with the server using the commands below.

### Usage

You can either execute the `demo.sh` script or execute the following commands:

#### Purposes

```bash
# Create a Purpose
curl \
-d '@config/purpose_config.json' \
-H 'Content-Type: application/json' \
-X POST \
'http://127.0.0.1/purposes'

# Get a Purpose
curl \
-X GET \
'http://127.0.0.1/purposes/[INSERT PURPOSE ID]'

# Delete a Purpose
curl \
-X DELETE \
'http://127.0.0.1/purposes/[INSERT PURPOSE ID]'
```

#### Apps

```bash
# Create a App
curl \
-d '@config/app_config.json' \
-H 'Content-Type: application/json' \
-X POST \
'http://127.0.0.1/apps'

# Get a App
curl \
-X GET \
'http://127.0.0.1/apps/[INSERT APP ID]'

# Delete a App
curl \
-X DELETE \
'http://127.0.0.1/apps/[INSERT APP ID]'
```

#### QoD Sessions

```bash
# Create a QoD Session
curl \
-d '@config/qod_config.json' \
-H 'Content-Type: application/json' \
-X POST \
'http://127.0.0.1/connectivity'

# Get a QoD Session
curl \
-X GET \
'http://127.0.0.1/connectivity/[INSERT SESSION ID]'

# Delete a QoD Session
curl \
-X DELETE \
'http://127.0.0.1/connectivity/[INSERT SESSION ID]'
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

## References

- https://mkjwk.org/
- https://8gwifi.org/jwkconvertfunctions.jsp
- https://jwt.io
- https://www.unixtimestamp.com/index.php