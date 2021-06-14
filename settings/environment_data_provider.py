import os
from sys import platform as _platform
from factory.utils.OsUtil import OsUtil
from factory.utils.FileUtil import FileUtil
from factory.utils.TextColorUtil import TextColor as Color


ENV_SETTINGS = "env_settings"
LINUX_OR_IOS = _platform == "linux" or _platform == "linux2" or _platform == "darwin"
WINDOWS = _platform == "win32" or "win64"
UTF8_UPPER = "UTF-8"
UTF8 = "utf-8"
SEP = os.sep


def read_env_conf_properties_to_os_platform(file_name):
    if LINUX_OR_IOS:
        return FileUtil.read_properties(
            [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir_name(), file_name)]
        )
    elif WINDOWS:
        return FileUtil.read_properties(
            [OsUtil.search_file_in_root_dir(OsUtil.get_current_dir(), file_name)]
        )


CONFIG = read_env_conf_properties_to_os_platform(ENV_SETTINGS + ".properties")


class EnvSettings:
    @staticmethod
    def get_screenshot_path():
        from factory.handling.allure_report_impl import allure_report_dir

        return str(f"{allure_report_dir}{SEP}screenshots")

    # ---- REPORT PARAMETERS ----
    @staticmethod
    def get_report_library_path():
        report_lib_path = os.path.abspath(CONFIG.get("report", "report_library_path"))
        return report_lib_path.replace("\\", SEP).strip()

    @staticmethod
    def get_generate_report():
        report_enabled = CONFIG.get("report", "generate_report", fallback=None)
        return str(report_enabled).strip() == "true"

    # ---- DEFAULT PARAMETERS ----
    @staticmethod
    def get_db_user():
        return CONFIG.get("default", "db_user").strip()

    @staticmethod
    def get_db_password():
        return CONFIG.get("default", "db_password").strip()

    @staticmethod
    def get_db_type():
        return CONFIG.get("default", "db_type").strip()

    @staticmethod
    def get_db_host():
        return CONFIG.get("default", "db_host").strip()

    @staticmethod
    def get_db_name():
        return CONFIG.get("default", "db_name").strip()

    @staticmethod
    def get_db_driver_abs_path():
        return CONFIG.get("default", "db_driver_abs_path").strip()

    # ---- DEBUG PARAMETERS ----
    @staticmethod
    def get_dev_mode():
        return CONFIG.get("cli-args-debug", "development_mode", fallback=None)

    @staticmethod
    def get_debug_flag_environment(default_env):
        env_config = CONFIG.get("cli-args-debug", "debug_flag_environment", fallback=None)
        environment_set = default_env if env_config is None else env_config
        return environment_set

    @staticmethod
    def get_debug_flag_target():
        return str(CONFIG.get("cli-args-debug", "debug_flag_target", fallback=None).strip())

    @staticmethod
    def get_debug_flag_mode():
        return str(CONFIG.get("cli-args-debug", "debug_flag_mode", fallback=None).strip())

    @staticmethod
    def get_debug_behave_tags():
        return CONFIG.get("cli-args-debug", "debug_behave_tags", fallback=None)

    @staticmethod
    def get_debug_behave_excluded_tags():
        return CONFIG.get("cli-args-debug", "debug_behave_excluded_tags", fallback=None)

    @staticmethod
    def get_debug_flag_os():
        return str(CONFIG.get("cli-args-debug", "debug_flag_os", fallback=None).strip())

    @staticmethod
    def get_debug_flag_os_version():
        return str(CONFIG.get("cli-args-debug", "debug_flag_os_version", fallback=None).strip())

    @staticmethod
    def show_logo():
        logo = Color.blue(
            """
                                              █                                                             
                            █████████.     :██                                                             
                         █████      ███    ███                                                              
                       ███           ██   ██                 .█.                                            
                     ███             ██  ██               █████████                ,█:                      
                   ███              :█: ██               ██       :██           :███████                    
                  ██               ███  ██        ████  ██     ███  ███       ███,    ,█:   ,████:          
                :██              ███:   ██      ███ ,█  ██       ██   ██    ███        ██ ████::█████:      
               ███         :██████      ███ :████   ██   ██     :█:    ██:███          ,███          ███:   
              ███                        :████     ██     ████████      ███                            :██: 
             ██:                                  ██        `█´                                          : 
            ██:                                  ██                                                         
           :██                                  ██              ,████        █████        ██ 
           ██                                 ,██              █     █      █     █        █ 
          ██                                 ███               █           █      █        █  
         ██                                 ███                █████       █:     █        █       
         ██                                ██                       █      █      █        █
        ██                               :██                      ,█       █    ,█         █     ,█   
        █                                +█                  .█████´        ████████      ████████   
            
                     PYON BEHAVE - SQL Test Automation | Created by: Hudson S. S. Rosa 
        
        """
        )
        """ Generated with http://manytools.org/hacker-tools/convert-images-to-ascii-art/go/ """
        return print(logo)
