#!/usr/bin/env node
import { App } from 'aws-cdk-lib';
import { MecStack } from "../lib/mec-stack";

const app = new App();

const mecStackCDG = new MecStack(app, "MecStackCDG", {
  az: 'eu-west-3a',
  wlz: 'eu-west-3-pilot-1a',
  keyname: 'eu-west-3',
  vpcCIDR: '172.26.0.0/16',
  publicAZSubnetCIDR: '172.26.128.0/18',
  publicWLZSubnetCIDR: '172.26.0.0/17',
  bastionhostImageId: 'ami-0afd55c0c8a52973a',
  bastionhostInstanceType: 't2.micro',
  publicWLZInstance1ImageId: 'ami-0afd55c0c8a52973a',
  publicWLZInstance1Type: 'g4dn.2xlarge',
  publicWLZInstance2ImageId: 'ami-0afd55c0c8a52973a',
  publicWLZInstance2Type: 'g4dn.2xlarge',
  env: {
      region: 'eu-west-3'
  },
});

const mecStackDFW = new MecStack(app, "MecStackDFW", {
  az: 'us-east-1a',
  wlz: 'us-east-1-wl1-dfw-wlz-1',
  keyname: 'manual-us-east-1',
  vpcCIDR: '172.26.0.0/16',
  publicAZSubnetCIDR: '172.26.128.0/18',
  publicWLZSubnetCIDR: '172.26.0.0/17',
  bastionhostImageId: 'ami-08c40ec9ead489470',
  bastionhostInstanceType: 't2.micro',
  publicWLZInstance1ImageId: 'ami-08c40ec9ead489470',
  publicWLZInstance1Type: 'g4dn.2xlarge',
  publicWLZInstance2ImageId: 'ami-08c40ec9ead489470',
  publicWLZInstance2Type: 'g4dn.2xlarge',
  env: {
      region: 'us-east-1'
  },
});
