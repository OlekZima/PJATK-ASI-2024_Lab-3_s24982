# Feature Engineering

## Data encoding

### Categorical values features

Categorical features was coded as:

!!! example "Changes"

    === "gender"

        ``` markdown
        Renamed to `gender_is_female`
        `female`: True
        `male`: False
        ```

    === "ethnicity"
        
        ``` markdown
        OneHotEncoded
        3 features were created:
        `ethnicity_afam` `ethnicity_hispanic` and `ethnicity_other`
        ```


    === "fcollege/mcollege"

        ``` markdown
        Renamed to `is_fcollege`/`is_mcollege`
        `yes`: True
        `no`: False
        ```
    
    === "home"
        
        ``` markdown
        Renamed to `is_home`
        `yes`: True
        `no`: False
        ```

    === "urban"
        
        ``` markdown
        Renamed to `is_urban`
        `yes`: True
        `no`: False
        ```

    === "income"
        
        ``` markdown
        Renamed to `is_high_income`
        `high`: True
        `low`: False
        ```

    === "region"
        
        ``` markdown
        Renamed to `is_region_west`
        `west`: True
        `other`: False
        ```


