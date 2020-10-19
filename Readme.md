cdk installtion

    Requiremnets

        - ubuntu machine ( x64 )

    Packages:
        
        - sudo apt update && sudo apt install python3 python3-pip -y
    
    Install cdk installtion:
        
        - pip3 install aws-cdk.cdk 
        - pip3 install awscli



verify cdk installtion:

        - cdk --version

configure aws credentials:

        - aws configure

    Stack Name:

        - S3bucketStack

           1. Create S3 bucket
           2. Upload the file into s3 bucket

        - LambdaCronStack

            1. create iam role ( dynamdb:*, s3bucket:*, cloudwatch:*, lambda:* )
            2. Lambdafunction Create
            3. Create event trigger function in cloudwatch

        - DynamoDbStack

            1. Create dynamodb

        <!-- - IamRoleStack

            1. Create iam role -->

Deploy procedures
    
    - cdk bootstrap ( Deploys the CDK toolkit stack into an AWS environment )

        cdk bootstrap -b vijaycdktestenv (To specify the s3 bucket name)

    - cdk synthesize  [stack alias name] ( to show script in the form cloudformatio format) (test)

    - cdk synthesize s3bucketCreationStack
    - cdk synthesize LambdaCron
    - cdk synthesize dynamodbCreationStack

parameter passing methods

    - cdk deploy [stack name] [stack name] [stack name] --parameters parametername=value

        Example: cdk deploy s3bucketCreationStack LambdaCron  dynamodbCreationStack --parameters uploadBucketName=vijays3bucketiotsss

Reference: 

- https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html
