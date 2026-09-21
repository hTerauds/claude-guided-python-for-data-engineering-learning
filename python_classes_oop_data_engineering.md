# Classes & OOP Basics for Data Engineering

## Learning goal

Understand the Python OOP concepts that are most useful for data
engineering, especially when you need to model something **stateful**
such as:

-   a pipeline configuration
-   a database connection wrapper
-   an API client
-   a file reader
-   a data validator

The goal is **not** to become an OOP expert yet. The key question is:

> Does this thing have state that should live together with the
> operations acting on that state?

If yes, a class is probably worth considering.

------------------------------------------------------------------------

# Part 1 --- \~20 min theory

## 1. The core idea: state + behavior

A class is a way to bundle:

-   **state** --- data that belongs to an object
-   **behavior** --- operations that work on that data

For example, imagine a database connection.

Its state might be:

``` python
host = "localhost"
database = "analytics"
connected = True
```

Its behavior might be:

``` python
connect()
disconnect()
execute_query()
```

A class lets us keep those things together:

``` python
class DatabaseConnection:
    def __init__(self, host, database):
        self.host = host
        self.database = database
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False
```

Then:

``` python
connection = DatabaseConnection("localhost", "analytics")

connection.connect()

print(connection.connected)  # True
```

The most important idea:

> **Object = state + operations that make sense for that state**

------------------------------------------------------------------------

## 2. Class vs object

A **class** is the blueprint.

``` python
class Pipeline:
    ...
```

An **object** is an actual instance created from that blueprint.

``` python
pipeline_1 = Pipeline()
pipeline_2 = Pipeline()
```

You can have many objects from one class:

``` text
Pipeline class
     │
     ├── pipeline_1
     │     ├── name = "users"
     │     └── status = "running"
     │
     └── pipeline_2
           ├── name = "orders"
           └── status = "failed"
```

The objects have the same structure but can have different state.

------------------------------------------------------------------------

## 3. `__init__` --- initializing an object

Usually you want an object to start with some state.

``` python
class Pipeline:
    def __init__(self, name, source):
        self.name = name
        self.source = source
        self.status = "created"
```

Now:

``` python
pipeline = Pipeline("users_pipeline", "postgres")

print(pipeline.name)
print(pipeline.source)
print(pipeline.status)
```

Output:

``` text
users_pipeline
postgres
created
```

`__init__` runs automatically when you create the object.

``` python
Pipeline("users_pipeline", "postgres")
```

Think of it as:

> "Create a new Pipeline object and initialize it with this data."

------------------------------------------------------------------------

## 4. What is `self`?

Consider:

``` python
class Pipeline:
    def __init__(self, name):
        self.name = name

    def run(self):
        print(f"Running {self.name}")
```

Then:

``` python
pipeline = Pipeline("users")

pipeline.run()
```

Inside `run()`, `self` refers to:

``` text
pipeline
```

So:

``` python
self.name
```

means:

> "The `name` belonging to this particular object."

For example:

``` python
pipeline_1 = Pipeline("users")
pipeline_2 = Pipeline("orders")
```

When you do:

``` python
pipeline_1.run()
```

`self` is `pipeline_1`.

When you do:

``` python
pipeline_2.run()
```

`self` is `pipeline_2`.

Therefore:

``` python
self.name
```

will be different.

------------------------------------------------------------------------

## 5. Attributes

Attributes are pieces of state stored on an object.

``` python
class Pipeline:
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule
        self.run_count = 0
```

You can access them:

``` python
pipeline.name
pipeline.schedule
pipeline.run_count
```

And modify them:

``` python
pipeline.run_count += 1
```

For a data engineer, common object state might look like:

``` python
connection.host
connection.port
connection.is_connected

pipeline.name
pipeline.source
pipeline.destination
pipeline.status

config.batch_size
config.retry_count
config.timeout
```

------------------------------------------------------------------------

## 6. Methods

A function defined inside a class is called a **method**.

``` python
class Pipeline:
    def __init__(self, name):
        self.name = name
        self.status = "created"

    def start(self):
        self.status = "running"

    def finish(self):
        self.status = "finished"
```

Now:

``` python
pipeline = Pipeline("users")

pipeline.start()
print(pipeline.status)

pipeline.finish()
print(pipeline.status)
```

Output:

``` text
running
finished
```

This is where OOP becomes useful.

Instead of doing:

``` python
pipeline["status"] = "running"
```

and separately writing:

``` python
start_pipeline(pipeline)
```

the object knows how to change its own state:

``` python
pipeline.start()
```

------------------------------------------------------------------------

## 7. A data-engineering example

Imagine you're writing a small ETL pipeline.

``` python
class ETLPipeline:
    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination
        self.status = "created"

    def run(self):
        self.status = "running"

        print(f"Extracting from {self.source}")
        print("Transforming data")
        print(f"Loading into {self.destination}")

        self.status = "completed"
```

Usage:

``` python
pipeline = ETLPipeline(
    "users_pipeline",
    "postgres",
    "data_warehouse"
)

pipeline.run()

print(pipeline.status)
```

The important part isn't the syntax.

It's the modeling:

``` text
ETLPipeline
│
├── state
│   ├── name
│   ├── source
│   ├── destination
│   └── status
│
└── behavior
    └── run()
```

That's a very common reason classes appear in data-engineering code.

------------------------------------------------------------------------

## 8. Why not just use dictionaries?

You absolutely **can** use dictionaries.

For example:

``` python
pipeline = {
    "name": "users",
    "source": "postgres",
    "destination": "s3",
    "status": "created"
}
```

And functions:

``` python
def start_pipeline(pipeline):
    pipeline["status"] = "running"
```

This is perfectly reasonable for simple data.

But as the system grows, you might end up with:

``` python
start_pipeline(pipeline)
validate_pipeline(pipeline)
stop_pipeline(pipeline)
retry_pipeline(pipeline)
get_pipeline_status(pipeline)
log_pipeline_run(pipeline)
```

A class can group the related behavior:

``` python
class Pipeline:
    def start(self):
        ...

    def validate(self):
        ...

    def stop(self):
        ...

    def retry(self):
        ...
```

Then:

``` python
pipeline.start()
pipeline.validate()
pipeline.retry()
```

This can make larger systems easier to organize.

------------------------------------------------------------------------

## 9. Stateful vs stateless

This distinction is particularly useful.

A **stateless function** doesn't need to remember anything between
calls.

``` python
def calculate_total(values):
    return sum(values)
```

You give it input:

``` python
calculate_total([1, 2, 3])
```

It gives you output.

No persistent internal state is necessary.

------------------------------------------------------------------------

A **stateful object** remembers something.

``` python
class Pipeline:
    def __init__(self):
        self.run_count = 0

    def run(self):
        self.run_count += 1
```

Now:

``` python
pipeline = Pipeline()

pipeline.run()
pipeline.run()
pipeline.run()

print(pipeline.run_count)
```

Output:

``` text
3
```

The object remembers what happened.

This is the key reason to reach for a class.

------------------------------------------------------------------------

## 10. Encapsulation --- don't worry too much yet

Another OOP term you'll hear is **encapsulation**.

The basic idea:

> Keep related state and behavior together, and control how that state
> is modified.

For example, suppose a connection should only be considered valid after
`connect()`.

Instead of having code everywhere doing:

``` python
connection.is_connected = True
```

you can make the class responsible:

``` python
class Connection:
    def __init__(self):
        self.is_connected = False

    def connect(self):
        # actual connection logic
        self.is_connected = True

    def disconnect(self):
        self.is_connected = False
```

Now the class controls the state transitions.

Don't worry about private attributes, getters/setters, etc. yet. Those
are useful later, but they're not the important part of today's lesson.

------------------------------------------------------------------------

## 11. Class attributes vs instance attributes

You'll occasionally see:

``` python
class Pipeline:
    pipeline_type = "ETL"
```

That's a **class attribute**.

It's shared by instances unless overridden.

More commonly you'll use instance attributes:

``` python
class Pipeline:
    def __init__(self, name):
        self.name = name
```

Each object gets its own `name`.

``` python
p1 = Pipeline("users")
p2 = Pipeline("orders")
```

So:

``` python
p1.name  # users
p2.name  # orders
```

For now, focus heavily on **instance attributes**.

------------------------------------------------------------------------

## 12. `__repr__` --- useful but optional

You may encounter this:

``` python
class Pipeline:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __repr__(self):
        return f"Pipeline(name={self.name!r}, status={self.status!r})"
```

Now:

``` python
pipeline = Pipeline("users", "running")

print(pipeline)
```

might produce:

``` text
Pipeline(name='users', status='running')
```

This is especially useful when debugging.

You don't need to memorize it yet.

------------------------------------------------------------------------

## 13. Inheritance --- learn the concept, don't overuse it

You will see code like:

``` python
class Pipeline:
    def run(self):
        print("Running pipeline")


class BatchPipeline(Pipeline):
    pass
```

`BatchPipeline` inherits from `Pipeline`.

So:

``` python
pipeline = BatchPipeline()
pipeline.run()
```

works.

You can also override behavior:

``` python
class StreamingPipeline(Pipeline):
    def run(self):
        print("Running streaming pipeline")
```

Inheritance is an important OOP concept, but **don't make it your main
focus as a beginner**.

In real data-engineering Python, you'll often get more value from
understanding:

-   classes
-   objects
-   attributes
-   methods
-   composition
-   simple interfaces
-   exceptions
-   context managers

than from building elaborate inheritance hierarchies.

------------------------------------------------------------------------

## 14. Composition --- especially useful for data engineering

Composition means one object contains another object.

Imagine:

``` python
class DatabaseConnection:
    def connect(self):
        print("Connected")


class Pipeline:
    def __init__(self, connection):
        self.connection = connection

    def run(self):
        self.connection.connect()
        print("Running pipeline")
```

Then:

``` python
connection = DatabaseConnection()

pipeline = Pipeline(connection)

pipeline.run()
```

The pipeline **has a connection**.

This is called a **has-a relationship**.

``` text
Pipeline
   │
   └── has a → DatabaseConnection
```

This pattern is extremely useful in data engineering.

You might eventually have:

``` text
Pipeline
├── DatabaseConnection
├── Logger
├── Config
└── DataValidator
```

rather than one giant class doing everything.

------------------------------------------------------------------------

## 15. When should you use a class?

A useful beginner decision rule:

### Use a function when:

You mostly have:

``` text
input → processing → output
```

Example:

``` python
def clean_email(email):
    return email.strip().lower()
```

No meaningful state needs to be remembered.

### Consider a class when:

You have something that:

1.  has **state**
2.  has **multiple operations**
3.  those operations naturally belong to that state

For example:

``` text
Database connection
    state:
        host
        database
        connected

    behavior:
        connect()
        disconnect()
        execute()
```

or:

``` text
Pipeline
    state:
        name
        source
        destination
        status
        run_count

    behavior:
        validate()
        run()
        retry()
```

That's the mental model to take away.

------------------------------------------------------------------------

## 16. The data-engineer mental model

When you see:

``` python
pipeline.run()
```

don't just think:

> "That's an OOP syntax thing."

Think:

> "There is an entity called `pipeline` that has state, and `run()` is
> an operation that changes or uses that state."

That's much more important.

------------------------------------------------------------------------

# Part 2 --- \~40 min practical challenge

We're going to build a small **ETL pipeline configuration + runner**.

Don't use pandas, databases, or external libraries. The goal is to
practice OOP itself.

## Challenge: Build a `Pipeline` class

Create a class representing a data pipeline.

### Requirements

Your class should be called:

``` python
Pipeline
```

It should have these attributes:

``` text
name
source
destination
batch_size
status
run_count
```

When a pipeline is created:

``` python
pipeline = Pipeline(
    name="users_pipeline",
    source="postgres",
    destination="warehouse",
    batch_size=1000
)
```

the initial state should be:

``` text
status = "created"
run_count = 0
```

------------------------------------------------------------------------

## Task 1 --- Create the class

Start with:

``` python
class Pipeline:
    def __init__(self, name, source, destination, batch_size):
        ...
```

Store the arguments as instance attributes.

You should be able to do:

``` python
pipeline = Pipeline(
    "users_pipeline",
    "postgres",
    "warehouse",
    1000
)

print(pipeline.name)
print(pipeline.source)
print(pipeline.destination)
print(pipeline.batch_size)
print(pipeline.status)
print(pipeline.run_count)
```

Expected:

``` text
users_pipeline
postgres
warehouse
1000
created
0
```

**Time: \~5 min**

------------------------------------------------------------------------

## Task 2 --- Add `validate()`

Add:

``` python
validate()
```

It should verify:

-   `name` isn't empty
-   `source` isn't empty
-   `destination` isn't empty
-   `batch_size` is greater than 0

If everything is valid:

``` python
return True
```

Otherwise:

``` python
return False
```

Example:

``` python
pipeline = Pipeline(
    "users_pipeline",
    "postgres",
    "warehouse",
    1000
)

print(pipeline.validate())
```

Expected:

``` text
True
```

And:

``` python
bad_pipeline = Pipeline(
    "",
    "postgres",
    "warehouse",
    0
)

print(bad_pipeline.validate())
```

Expected:

``` text
False
```

**Time: \~7 min**

------------------------------------------------------------------------

## Task 3 --- Add `run()`

Add:

``` python
run()
```

The method should:

1.  Validate the pipeline.
2.  If validation fails, print:

``` text
Pipeline validation failed
```

and don't run anything.

3.  If validation succeeds:
    -   change status to `"running"`
    -   print something like:

``` text
Running pipeline: users_pipeline
Extracting from postgres
Transforming data
Loading into warehouse
```

-   increment `run_count`
-   change status to `"completed"`

Example:

``` python
pipeline.run()
```

Then:

``` python
print(pipeline.status)
print(pipeline.run_count)
```

Expected:

``` text
completed
1
```

Run it again:

``` python
pipeline.run()

print(pipeline.run_count)
```

Expected:

``` text
2
```

This is where you should notice the value of **stateful objects**.

The pipeline remembers:

``` python
run_count
```

between method calls.

**Time: \~10 min**

------------------------------------------------------------------------

## Task 4 --- Add `reset()`

Add:

``` python
reset()
```

It should change:

``` python
status = "created"
```

but **should not reset `run_count`**.

So:

``` python
pipeline.run()
pipeline.run()

print(pipeline.run_count)
# 2

pipeline.reset()

print(pipeline.status)
# created

print(pipeline.run_count)
# 2
```

Why might this make sense?

Because resetting the current pipeline state doesn't necessarily mean
forgetting its historical execution count.

**Time: \~5 min**

------------------------------------------------------------------------

## Task 5 --- Multiple pipelines

Create three pipelines:

``` text
users_pipeline
orders_pipeline
payments_pipeline
```

Give them different sources, destinations, and batch sizes.

For example:

``` text
users:
    postgres → warehouse

orders:
    mysql → warehouse

payments:
    api → warehouse
```

Run them independently.

Then print their state.

You should see that each object maintains its **own state**.

For example:

``` python
print(users_pipeline.run_count)
print(orders_pipeline.run_count)
print(payments_pipeline.run_count)
```

If you run:

``` python
users_pipeline.run()
users_pipeline.run()

orders_pipeline.run()
```

the result should be:

``` text
2
1
0
```

This is an important OOP concept.

Each instance has its own state.

**Time: \~5 min**

------------------------------------------------------------------------

## Task 6 --- Stretch challenge

Now add:

``` python
last_error
```

to the pipeline.

Initially:

``` python
last_error = None
```

Modify `run()` so that if validation fails, it stores a useful error
message.

For example:

``` python
last_error = "Batch size must be greater than 0"
```

Then:

``` python
pipeline = Pipeline(
    "users",
    "postgres",
    "warehouse",
    0
)

pipeline.run()

print(pipeline.last_error)
```

might produce:

``` text
Batch size must be greater than 0
```

**Time: \~8 min**

------------------------------------------------------------------------

# Bonus --- Make it feel more like real data engineering

Once you've completed everything above, try adding:

``` python
status_report()
```

It should return something like:

``` python
{
    "name": "users_pipeline",
    "status": "completed",
    "run_count": 3,
    "last_error": None
}
```

Then:

``` python
print(pipeline.status_report())
```

This introduces a useful pattern:

> An object manages state internally, while providing methods for other
> parts of the application to interact with that state.

------------------------------------------------------------------------

# One important rule for your learning

Don't try to turn everything into a class.

This:

``` python
def clean_column_name(name):
    return name.strip().lower().replace(" ", "_")
```

doesn't need a class.

But something like:

``` text
DatabaseConnection
Pipeline
APIClient
FileReader
KafkaConsumer
PipelineConfig
DataValidator
```

can naturally have **state + behavior**, so classes become useful.

A useful learning progression for data engineering is:

``` text
Functions
   ↓
Dictionaries / lists
   ↓
Classes + state
   ↓
Composition
   ↓
Exceptions
   ↓
Context managers
   ↓
Dataclasses
   ↓
Typing / protocols
```

You don't need advanced OOP before you can write useful data-engineering
Python.

The goal at this stage is simply to become comfortable asking:

> **"Does this thing have state that should live together with the
> operations acting on that state?"**

If yes, a class is probably worth considering.
