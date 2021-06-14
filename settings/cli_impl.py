import os
import argparse
from factory.base_context import BaseContext as Bctx
from factory.handling.base_logging import BaseLogging as Log
from settings.environment_data_provider import EnvSettings as Conf


class Cli:
    @staticmethod
    def parse_external_args():
        parser = argparse.ArgumentParser(usage="%(prog)s [options]")
        parser.add_argument(
            "--environment",
            choices=["staging", "dev", "production"],
            help="==> Environment to execute the tests (default = staging). Find the app URLs in properties file",
            default="staging",
        )
        parser.add_argument(
            "--target",
            choices=["local"],
            help="==> Platform to execute the tests (default = local)",
            default="local",
        )
        parser.add_argument(
            "--mode",
            choices=["mysql", "oracle"],
            help="==> RDBMS to be connected (default = mysql)",
            default="mysql",
        )
        parser.add_argument(
            "--os",
            choices=[
                "MacOS High Sierra",
                "MacOS Catalina",
                "MacOS Big sur",
                "Windows",
                "Windows 10",
                "iOS",
                "Android",
                "",
            ],
            type=str,
            help="==> Operational System from the current server",
            default="MacOS Catalina",
        )
        parser.add_argument(
            "--os_version",
            choices=[
                "14.3",
                "14.0",
                "14",
                "13.0",
                "13",
                "12.0",
                "12",
                "11.0",
                "11",
                "10.0",
                "10",
                "9.0",
                "9",
                "8.1",
                "8.0",
                "8",
                "7.1",
                "7.0",
                "7",
                "6.0",
                "6",
                "5.0",
                "5",
                "4.4",
                "",
            ],
            type=str,
            help="==> Preferably use XX.X for mobile and XX for OS platform versions",
            default="",
        )
        parser.add_argument(
            "--tags",
            help="==> Feature(s) / Scenario(s) to be executed (separate tags by comma and without spaces)",
            default="",
        )
        parser.add_argument(
            "--exclude",
            choices=["wip", "skip", "bug", "slow", "obsolete", ""],
            help="==> Feature(s) / Scenario(s) to be ignored / skipped from execution using a single tag (recommended: wip)",
            default="",
        )
        args = parser.parse_args()
        return args

    @staticmethod
    def set_arguments(args):
        check_flags = (
            lambda arg_cmd, config_var: config_var
            if Conf.get_dev_mode().strip() == "true"
            else str(arg_cmd)
        )
        notify_running_mode = (
            Log.info(
                "<<<<< DEV MODE ENABLED: Using capabilities set from 'env_settings.properties' >>>>>\n"
            )
            if Conf.get_dev_mode().strip() == "true"
            else ""
        )
        flag_target = check_flags(args.target, Conf.get_debug_flag_target())
        flag_os = check_flags(args.os, Conf.get_debug_flag_os())
        flag_os_version = check_flags(args.os_version, Conf.get_debug_flag_os_version())
        flag_mode = check_flags(args.mode, Conf.get_debug_flag_mode())
        flag_tags = check_flags(str(args.tags).rstrip(",").strip(), Conf.get_debug_behave_tags())
        flag_exclude = check_flags(
            str(args.exclude).rstrip(",").strip(), Conf.get_debug_behave_excluded_tags()
        )
        flag_environment = check_flags(args.environment, Conf.get_debug_flag_environment("staging"))

        Bctx.flag_mode.set(flag_mode)
        Bctx.flag_exclude.set(flag_exclude)
        Bctx.flag_os.set(flag_os)
        Bctx.flag_os_version.set(flag_os_version)
        Bctx.flag_tags.set(flag_tags)
        Bctx.flag_target.set(flag_target)
        Bctx.flag_environment.set(flag_environment)

        os.environ["environment"] = Bctx.flag_environment.get()
        os.environ["exclude"] = Bctx.flag_exclude.get()
        os.environ["mode"] = Bctx.flag_mode.get()
        os.environ["os"] = Bctx.flag_os.get()
        os.environ["os_version"] = Bctx.flag_os_version.get()
        os.environ["tags"] = Bctx.flag_tags.get()
        os.environ["target"] = Bctx.flag_target.get()

        Conf.show_logo()
        Log.info(
            f"Running with commands: \n\n \
                    EXECUTION TYPE: \n \
                    - Target = {Bctx.flag_target.get()} \n \
                    - Mode = {Bctx.flag_mode.get()} \n\n \
                    PLATFORM: \n \
                    - OS = {Bctx.flag_os.get()} \n \
                    - OS Version = {Bctx.flag_os_version.get()} \n \
                    APPLICATION: \n \
                    - Environment = {Bctx.flag_environment.get()} \n \
                    TESTS: \n \
                    - Behave Tag(s) = {Bctx.flag_tags.get()} \n \
                    - Behave Excluded Tags = {Bctx.flag_exclude.get()} \n"
        )

    @staticmethod
    def parse_behave_tags(tags_sequence=""):
        tags_sequence = Bctx.flag_tags.get()
        if tags_sequence is None or tags_sequence == "":
            return ""
        else:
            return "--tags=" + tags_sequence.replace(" ", "").replace("@", "").lower().strip() + " "

    @staticmethod
    def get_arguments():
        return {
            "environment": os.environ["environment"],
            "exclude": os.environ["exclude"],
            "mode": os.environ["mode"],
            "os": os.environ["os"],
            "os_version": os.environ["os_version"],
            "tags": os.environ["tags"],
            "target": os.environ["target"],
        }
