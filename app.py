from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3upload,
    core,
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_dynamodb,
    aws_iam,
)


class S3bucketStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        _bucket_name = core.CfnParameter(self, "uploadBucketName", type="String",
                                               description="To pass s3 bucket name")

        ZipFIleName = "index.zip"

        # bucket Creation
        bucket = s3.Bucket(self,
                           "s3bucketCreation",
                           bucket_name=_bucket_name.value_as_string,
                           public_read_access=False,
                           versioned=True
                           )

        # fileUpload after bucket creation
        UpLoad = s3upload.BucketDeployment(self,
                                           "s3bucketCreationAfterUpload",
                                           destination_bucket=bucket,
                                           sources=[
                                               s3upload.Source.asset(ZipFIleName)]
                                           )

        iamRole = aws_iam.Role(self, "lambdaUniqueID", role_name="lamdaFuncPythonc", assumed_by=aws_iam.ServicePrincipal(
            "lambda.amazonaws.com"))

        iamRole.add_to_policy(aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["logs:CreateLogGroup",
                     "logs:CreateLogStream",
                     "logs:PutLogEvents",
                     "cloudwatch:*",
                     "dynamodb:*",
                     "s3:*"],
            resources=["*"]
        ))

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "Singleton",
            function_name="lamdaFuncPython",
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole

        )

        # Run Every 5 minutes between 8:00 AM and 5:55 PM weekdays
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            rule_name="lamdaFuncPythonRule",
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='5-17',
                month='*',
                week_day='SUN-FRI',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFunction))


        # OutPut Section
        core.CfnOutput(self, "bucket_name", value=bucket.bucket_name)

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            table_name="lamdafunctiondynamitl",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )



app = core.App()
S3bucketStack(app, "s3bucketCreationStack")
app.synth()
