class Pipeline:
    #name
    #source
    #destination
    #batch_size
    #status
    #run_count
    def __init__(self, name, source, destination, batch_size):
        self.name = name
        self.source = source
        self.destination = destination
        self.batch_size = batch_size
        self.status = "created"
        self.run_count = 0
        self.last_error = None
    def validate(self):
        if self.name != "" and self.source != "" and self.destination != "" and self.batch_size > 0:
            print(True)
        else:
            print(False)
    def run(self):
        if self.validate():
            self.status = "running"
            print(f"Running pipeline: {self.name}")
            print(f"Extracting from {self.source}")
            print("Transforming data")
            print (f"Loading into {self.destination}")
            self.run_count += 1
            self.status = "completed"
        else:
            if self.name == "": self.last_error = "Pipeline must have name"
            if self.source == "": self.last_error = "Pipeline must have source"
            if self.destination == "": self.last_error = "Pipeline must have destination"
            if self.batch_size <= 0: self.last_error = "Batch size must be greater than 0"
            print('Pipeline validation failed, error stored')
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
    
users_pipeline = Pipeline(name="users_pipeline", source="postgres", destination="warehouse", batch_size=100)
orders_pipeline = Pipeline(name="orders_pipeline", source="mysql", destination="warehouse", batch_size=1)
payments_pipeline = Pipeline(name="payments_pipeline", source="api", destination="warehouse", batch_size=20)

users_pipeline.run()
orders_pipeline.run()
users_pipeline.run()
users_pipeline.run()
orders_pipeline.run()
payments_pipeline.run()
print (users_pipeline.run_count)
print (orders_pipeline.run_count)
print (payments_pipeline.run_count)

print (users_pipeline.last_error)
print (orders_pipeline.last_error)
print (payments_pipeline.last_error)

print (users_pipeline.status_report())
print (orders_pipeline.status_report())
print (payments_pipeline.status_report())