import subprocess
import logging
from pathlib import Path
import os
from install_dependencies import check_bash, check_java

def idml2hubxml(input, **options):
    logging.info("idml2hubxml starting...")

    bash_version = check_bash()
    if (bash_version == -1):
        e = RuntimeError("Your bash version is too old. Please update it (>= 5.0.0) or point to a more recent version in your .env file.")
        raise e
    else: logging.info(f"bash version used: {bash_version}.")

    java_version = check_java()
    if (java_version == -1):
        e = RuntimeError("Your Java version is too old. Please update it (>= 7.0.0).")
        raise e
    else: logging.info(f"Java version used: {java_version}.")

    filename = Path(input).stem

    output_folder = options["idml2hubxml_output"]

    if options["idml2hubxml_script"] is None:
        e = NameError("Your .env file is missing the IDML2HUBXML_SCRIPT_FOLDER entry")
        logging.error(e)
        raise e
    else:
        cmd = [os.getenv("BASH"), options["idml2hubxml_script"] + "/idml2xml.sh", "-o", output_folder, input]
        logging.info("Now running: " + " ".join(cmd))
        subprocess.run(cmd, capture_output=True) # comment out this line to just get the previous run of idml2xml

    outputfile = output_folder + "/" + filename + ".xml"
    logfile = output_folder + "/" + filename + ".log"

    logging.info("Output of idml2xml written at: " + outputfile)
    logging.info("idml2xml log file written at: " + logfile)
    logging.info("idml2hubxml done.")
    return outputfile