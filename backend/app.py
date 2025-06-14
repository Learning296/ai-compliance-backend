from flask import Flask, request, jsonify
from flask_cors import CORS
from auditpilot.core.ai_analyzer import AISecurityAssessment

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow frontend communication
CORS(app)

# Instantiate our assessment engine
assessor = AISecurityAssessment()

@app.route('/api/assess', methods=['POST'])
def assess():
    """
    API endpoint to receive assessment data, run it through the engine,
    and return a comprehensive report.
    """
    try:
        # Get the assessment data from the request body
        assessment_data = request.get_json()
        if not assessment_data:
            return jsonify({"error": "Invalid input: No data provided"}), 400

        # Generate the report using our core engine
        report = assessor.generate_assessment_report(assessment_data)

        # Return the report as a JSON response
        return jsonify(report)

    except Exception as e:
        # Handle any errors that occur during the process
        return jsonify({"error": "An error occurred during assessment", "details": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5001 to avoid conflicts with other services
    app.run(debug=True, port=5001) 