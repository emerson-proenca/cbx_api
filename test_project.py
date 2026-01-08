# myapp.py
import logging



def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    logging.debug("This is a debug")
    logging.info("information!!")



if __name__ == "__main__":
    main()
