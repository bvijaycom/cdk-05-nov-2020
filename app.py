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


class firstStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        # input variable Section

        _bucket_name = core.CfnParameter(
            self, "uploadBucketName", type="String")
        _bucket_folder_name=core.CfnParameter(self, "LambdaName", type="String")
        _lambda_name = core.CfnParameter(self, "LambdaName", type="String")
        _dynamodb_name = core.CfnParameter(self, "DynamodbName", type="String")

        _lambda_Role_name = _lambda_name.value_as_string + 'Role'
        _lambda_Rule_name = _lambda_name.value_as_string + 'Rule'

        ZipFIleName = core.CfnParameter(self, "uploadZipfileName", type="String")
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
                                           destination_key_prefix="web/static",
                                           sources=[
                                               s3upload.Source.asset(ZipFIleName.value_as_string)]
                                           )

        iamRole = aws_iam.Role(self,
                               "lambdaUniqueID",
                               role_name=_lambda_Role_name,
                               assumed_by=aws_iam.ServicePrincipal(
                                   "lambda.amazonaws.com")
                               )

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

        with open("lambdafiles/lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "Singleton",
            function_name=_lambda_name.value_as_string,
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
            rule_name=_lambda_Rule_name,
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='*',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFunction))

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "demo_table",
            table_name=_dynamodb_name.value_as_string,
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # OutPut Section
        core.CfnOutput(self, "bucket_name", value=bucket.bucket_name)
        core.CfnOutput(self, "Lamda_Name", value=bucket.bucket_name)
        core.CfnOutput(self, "dynamedbName", value=demo_table.table_name)


app = core.App()
firstStack(app, "S3dlCreationStack")
app.synth()
