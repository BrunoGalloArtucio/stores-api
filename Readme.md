# Items

-   `Flask` app configured in `app.py`

### Authentication

-   Routes protected with `@jwt_required()`
-   Extra error handlers `expired_token_loader`, `invalid_token_loader`, and `unauthorized_loader` added in `app.py`
-   Claims added to jwt token by `additional_claims_loader` in `app.py`
-   Custom `admin_required` decorator defined in `decorators.py`
-   We enable a `refresh` endpoint so that clients can use our API without needing to constantly log back in every time tokens expire. Instead, they can call this endpoint with the `refresh_token` returned in the log in response. The `refresh` endpoint returns a non-fresh token, that still can be used to access most of our API. However, if the user needs to perform a critical operation, like deleting their account, they'll need a fresh token, which they can obtain via logging in again.
