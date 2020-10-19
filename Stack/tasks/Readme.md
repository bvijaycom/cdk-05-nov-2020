Stack Details:
    
    S3bucket

        1. Create S3 bucket
        2. Upload the file into s3 bucket

    LambdaCron

        1. create iam role ( dynamdb:*, s3bucket:*, cloudwatch:*, lambda:* )
        2. Lambdafunction Create
        3. Create event trigger function in cloudwatch

    DynamoDb

        1. Create dynamodb

Deploy procedures
    
    cdk bootstrap -b [unique s3backetname] 
    cdk list
    cdk synthesize  

First Stack deploy

    cdk deploy First-Stack --parameters uploadBucketName=jinojoes3bucket \
        --parameters DynamodbName=jinojoeDynamodb \
        --parameters targetFoldername='common' \
        --parameters FirstLambdaName=firstlambda \
        --parameters uploadZipfileName='files' 

Second Stack Deploy

    cdk deploy Second-Stack --parameters SecondLambdaName=secondlambda 

Third Stack Deploy

    cdk deploy Third-Stack --parameters ThirdLambdaName=thirdlambda 

Fourth Stack Deploy

    cdk deploy Fourth-Stack --parameters FourthLambdaName=fourthlambda 
