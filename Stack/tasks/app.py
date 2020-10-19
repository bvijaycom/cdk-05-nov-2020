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


class FirstStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        # input variable Section

        _bucket_name = core.CfnParameter(self, "uploadBucketName", type="String")
        _bucket_folder_name = core.CfnParameter(self, "targetFoldername", type="String")
        first_lambda_name = core.CfnParameter(self, "FirstLambdaName", type="String")
        _dynamodb_name = core.CfnParameter(self, "DynamodbName", type="String")
        ZipFIleNames = core.CfnParameter(self, "uploadFoldername", type="String")

        first_lambda_Role_name = first_lambda_name.value_as_string + 'Role'
        first_lambda_Rule_name = first_lambda_name.value_as_string + 'Rule'

        # bucket Creation

        bucket = s3.Bucket(self,
                           "oneone",
                           bucket_name=_bucket_name.value_as_string,
                           public_read_access=False,
                           versioned=True
                           )

        # fileUpload after bucket creation

        UpLoad = s3upload.BucketDeployment(self,
                                           "onetwo",
                                           destination_bucket=bucket,
                                           destination_key_prefix=_bucket_folder_name.value_as_string,
                                           sources=[
                                               s3upload.Source.asset(ZipFIleNames.value_as_string)]
                                           )

        iamRole = aws_iam.Role(self,
                               "onethree",
                               role_name=first_lambda_Role_name,
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

        with open("files/lambda-handler1.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "onefour",
            function_name=first_lambda_name.value_as_string,
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole
        )


        rule = events.Rule(
            self, "onefive",
            rule_name=first_lambda_Rule_name,
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='*',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFunction))

        # create dynamo table
        dynamo_table = aws_dynamodb.Table(
            self, "onesix",
            table_name=_dynamodb_name.value_as_string,
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # OutPut Section
        core.CfnOutput(self, "bucket_name", value=bucket.bucket_name)
        core.CfnOutput(self, "_FirstLambdaName", value=lambdaFunction.function_name)
        core.CfnOutput(self, "dynamodbName", value=dynamo_table.table_name)


class SecondStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        second_lambda_name = core.CfnParameter(self, "SecondLambdaName", type="String")
        second_lambda_Role_name = second_lambda_name.value_as_string + 'Role'
        second_lambda_Rule_name = second_lambda_name.value_as_string + 'Rule'

        iamRole = aws_iam.Role(self,
                               "twoone",
                               role_name=second_lambda_Role_name,
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

        with open("files/lambda-handler2.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "twotwo",
            function_name=second_lambda_name.value_as_string,
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole
        )

        rule = events.Rule(
            self, "twothree",
            rule_name=second_lambda_Rule_name,
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='*',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFunction))

        core.CfnOutput(self, "_SecondLambdaName", value=lambdaFunction.function_name)


class ThreeStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        third_lambda_name = core.CfnParameter(
            self, "ThirdLambdaName", type="String")
        third_lambda_Role_name = third_lambda_name.value_as_string + 'Role'
        third_lambda_Rule_name = third_lambda_name.value_as_string + 'Rule'

        iamRole = aws_iam.Role(self,
                               "threeone",
                               role_name=third_lambda_Role_name,
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

        with open("files/lambda-handler3.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "threetwo",
            function_name=third_lambda_name.value_as_string,
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole
        )

        rule = events.Rule(
                self, "threethree",
                rule_name=third_lambda_Rule_name,
                schedule=events.Schedule.cron(
                    minute='0/5',
                    hour='*',
                    month='*',
                    week_day='MON-FRI',
                    year='*'),
            )

        rule.add_target(targets.LambdaFunction(lambdaFunction))

        core.CfnOutput(self, "_ThirdLambdaName", value=lambdaFunction.function_name)


class FourStack(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        fourth_lambda_name = core.CfnParameter(self, "FourthLambdaName", type="String")
        fourth_lambda_Role_name = fourth_lambda_name.value_as_string + 'Role'
        fourth_lambda_Rule_name = fourth_lambda_name.value_as_string + 'Rule'


        iamRole = aws_iam.Role(self,
                               "fourone",
                               role_name=fourth_lambda_Role_name,
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

        with open("files/lambda-handler4.py", encoding="utf8") as fp:
            handler_code = fp.read()

        lambdaFunction = lambda_.Function(
            self, "fourtwo",
            function_name=fourth_lambda_name.value_as_string,
            code=lambda_.InlineCode(handler_code),
            handler="index.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            role=iamRole
        )


        rule = events.Rule(
            self, "fourthree",
            rule_name=fourth_lambda_Rule_name,
            schedule=events.Schedule.cron(
                minute='0/5',
                hour='*',
                month='*',
                week_day='MON-FRI',
                year='*'),
        )

        rule.add_target(targets.LambdaFunction(lambdaFunction))

        core.CfnOutput(self, "_FourthLambdaName", value=lambdaFunction.function_name)



app = core.App()
FirstStack(app, "FirstStack")
SecondStack(app, "SecondStack")
ThreeStack(app, "ThirdStack")
FourStack(app, "FourthStack")
app.synth()