import subprocess
import logging
from pathlib import Path

def idml2hubxml(input, **options):
    logging.info("idml2hubxml starting...")

    filename = Path(input).stem

    output_folder = options["idml2hubxml_output"]

    if options["idml2hubxml_script"] is None:
        e = NameError("Your .env file is missing the IDML2HUBXML_SCRIPT_FOLDER entry")
        logging.error(e)
        raise e
    else:
        cmd = ["bash", options["idml2hubxml_script"] + "/idml2xml.sh", "-o", output_folder, input]
        logging.info("Now running: " + " ".join(cmd))
        subprocess.run(cmd, capture_output=True) # comment out this line to just get the previous run of idml2xml

    outputfile = output_folder + "/" + filename + ".xml"
    logfile = output_folder + "/" + filename + ".log"

    logging.info("Output of idml2xml written at: " + outputfile)
    logging.info("idml2xml log file written at: " + logfile)
    logging.info("idml2hubxml done.")
    return outputfile