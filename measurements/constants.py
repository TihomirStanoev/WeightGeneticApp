class MeasurementValidationErrorMessages:
    WEIGHT_GR_MESSAGE = 'Weight must be greater than zero.'
    LENGTH_MM_MESSAGE = 'Measured length must be greater than zero.'
    LENGTH_OUT_OF_RANGE = 'Measured length {length:.2f} mm is outside allowed range [{low:.2f}, {high:.2f}] mm.'
    WEIGHT_OUT_OF_RANGE = 'Measured weight {value:.2f} gr for {field_name} is outside allowed range [{low:.2f}, {high:.2f}] gr.'