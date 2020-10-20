| S3bucket | Lambda | DynamoDb |
| --------------- | --------------- | --------------- |
| 1. Create S3 bucket| 1. create iam role | 1. Create dynamodb |
| 2. Upload the file into s3 bucket | 2. Lambdafunction Create |  |
|  | 3. Create event trigger function in cloudwatch |  |

| Operating System |
| --------------- |
| ubuntu machine ( x64 ) |
        
| Dependencies Packages |
| --------------- |
| sudo apt update |
| sudo apt install python3 python3-pip -y |


| cdk installtion |
| --------------- |
| pip3 install aws-cdk.cdk |
| pip3 install awscli |

| verify cdk installtion |
| --------------- |
| cdk --version |

| configure aws credentials |
| --------------- |
| aws configure |



Reference: 

- https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html
- https://pypi.org/project/aws-cdk.aws-s3-deployment/
- https://docs.aws.amazon.com/cdk/api/latest/python/index.html
