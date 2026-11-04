import connexion

app = connexion.FlaskApp(__name__)

app.add_api(
    "openapi.yaml",
    strict_validation=True,
    validate_responses=True
)

if __name__ == "__main__":
    app.run(port=5000, debug=True)