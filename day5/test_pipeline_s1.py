from day4.s1_pipeline_class import Pipeline
#def test_pipeline_initial_state():
#    p=Pipeline(name="",source="source_name",destination="destination_name",batch_size=1)
#    assert p.validate() == False
def test_validate_validate_function():
    # Arrange: set up what you're testing
    p = Pipeline(name="qqq", source="db", destination="wh", batch_size=10)
    # Act: do the thing
    val = p.validate()
    result = True if "Pipeline is succesfuly validated" in val else False
    # Assert: check the result
    assert result == True
def test_pipeline_initial_state():
    # Arrange: set up what you're testing
    p = Pipeline(name="qqq", source="db", destination="wh", batch_size=10)
    # Act: do the thing
    # Assert: check the result
    assert p.status == "created" and p.run_count == 0
def test_piplene_validate_truthy_response_msg():
    # Arrange: set up what you're testing
    #name/source/destination/batch_size
    p = Pipeline(name="ok_name", source="ok_source", destination="ok_destination", batch_size=10)
    
    # Act: do the thing
    truthy_validation_result = (
        True if "Pipeline is succesfuly validated" in p.validate()
        else False
    )
    # Assert: check the result
    assert truthy_validation_result
def test_validate_missing_name():
    # Arrange: set up what you're testing
    p = Pipeline(name="", source="ok_source", destination="ok_destination", batch_size=10)
    faulty_name_validation_result = (
            True if "Pipeline must have name (string with one or more elements)" in p.validate()
            else False
        )
    assert faulty_name_validation_result
def test_validate_zero_batch_size():
    p = Pipeline(name="ok_name", source="ok_source", destination="ok_destination", batch_size=0)
    faulty_batch_size_validation_result = (
        True if "Batch size must be greater than 0" in p.validate() 
        else False
    )
    assert faulty_batch_size_validation_result
def test_run_increments_run_count():
    p = Pipeline(name="ok_name", source="ok_source", destination="ok_destination", batch_size=10)
    p.run()
    assert p.run_count ==1
def test_run_twice_increments_twice():
    p = Pipeline(name="ok_name", source="ok_source", destination="ok_destination", batch_size=10)
    p.run()
    p.run()
    assert p.run_count ==2
def test_status_report_shape():
    p = Pipeline(name="ok_name", source="ok_source", destination="ok_destination", batch_size=10)
    report = p.status_report()
    assert {"name", "status", "run_count", "last_error"} <= report.keys()
    