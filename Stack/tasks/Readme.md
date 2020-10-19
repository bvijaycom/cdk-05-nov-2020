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

parameter passing methods

    cdk deploy FirstStack SecondStack ThirdStack FourthStack \
        --parameters uploadBucketName=jinojoes3bucket \
        --parameters DynamodbName=jinojoeDynamodb \
        --parameters uploadZipfileName='../files' \
        --parameters targetFoldername='common' \
        --parameters FirstLambdaName=jinojoelambda \
        --parameters SecondLambdaName=jinojoelambda \
        --parameters ThirdLambdaName=jinojoelambda \
        --parameters FourthLambdaName=jinojoelambda 
