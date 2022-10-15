from housing.pipeline.pipeline import Pipeline
from housing.logger import logging

def main():
    try:
        pipeline_obj=Pipeline()
        pipeline_obj.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()
