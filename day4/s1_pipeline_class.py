class Pipeline:
    def __init__(self, name, source, destination, batch_size):
        self.name = name
        self.source = source
        self.destination = destination
        self.batch_size = batch_size
        self.status = "created"
        self.run_count = 0
        self.errors = []
        self.last_error = None
    def validate(self):
        faulty_name_msg = (
            "Pipeline must have name (string with one or more elements)"
            if self.name == ""
            else None
        )
        faulty_source_msg = (
            "Pipeline must have source name (string with one or more elements)"
            if self.source == ""
            else None
        )
        faulty_destination_msg = (
            "Pipeline must have destination name (string with one or more elements)"
            if self.destination == ""
            else None
        )
        faulty_batch_size_msg = (
            "Batch size must be greater than 0"
            if self.batch_size <=0
            else None
        )
        if self.name != "" and self.source != "" and self.destination != "" and self.batch_size > 0:
            result = ("Pipeline is succesfuly validated",)
        else:
            result = (faulty_name_msg, faulty_source_msg, faulty_destination_msg, faulty_batch_size_msg)
        return result
    def run(self):
        if "Pipeline is succesfuly validated" in self.validate():
            self.status = "running"
            print(f"Running pipeline: {self.name}")
            print(f"Extracting from {self.source}")
            print("Transforming data")
            print (f"Loading into {self.destination}")
            self.run_count += 1
            self.status = "completed"
        else:
            if self.name == "": self.last_error = "Pipeline must have name"; self.errors.append("Pipeline must have name")
            if self.source == "": self.last_error = "Pipeline must have source"; self.errors.append("Pipeline must have source")
            if self.destination == "": self.last_error = "Pipeline must have destination"; self.errors.append("Pipeline must have destination")
            if self.batch_size <= 0: self.last_error = "Batch size must be greater than 0"; self.errors.append("Batch size must be greater than 0")
            print('Pipeline validation failed, error/rs stored')
    def reset(self):
        self.status("created")
    def status_report(self):
        status = {
                "name": self.name,
                "status": self.status,
                "run_count": self.run_count,
                "last_error": self.last_error
            }
        return status

if __name__ =="__main__":
    users_pipeline = Pipeline(name="", source="", destination="", batch_size=0)
    orders_pipeline = Pipeline(name="orders_pipeline", source="mysql", destination="warehouse", batch_size=1)
    payments_pipeline = Pipeline(name="payments_pipeline", source="api", destination="warehouse", batch_size=20)
    result_type = orders_pipeline.validate()
    orders_pipeline.run()
    print (orders_pipeline.run_count)
    # users_pipeline.run()
    # users_pipeline.run()
    # orders_pipeline.run()
    # payments_pipeline.run()
    # print (users_pipeline.run_count)
    # print (orders_pipeline.run_count)
    # print (payments_pipeline.run_count)

    # print (users_pipeline.last_error)
    # print (orders_pipeline.last_error)
    # print (payments_pipeline.last_error)

    # print (users_pipeline.status_report())
    # print (orders_pipeline.status_report())
    # print (payments_pipeline.status_report())