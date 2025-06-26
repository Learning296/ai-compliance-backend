from flask import Flask, request, jsonify
from flask_cors import CORS
# Import both of our powerful classes
from auditpilot.core.ai_analyzer import AIComplianceAnalyzer, AISecurityAssessment
import os

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow frontend communication
CORS(app)

# Instantiate our engines
# The 'Thinker' that makes judgments
ai_thinker = AIComplianceAnalyzer()
# The 'Calculator' that does the math
score_calculator = AISecurityAssessment()

@app.route('/api/analyze_and_score', methods=['POST'])
def analyze_and_score():
    """
    A new, powerful endpoint that takes simple, natural language evidence,
    gets a base_score from the AI, calculates the final score, and returns everything.
    """
    try:
        data = request.get_json()
        if not data or 'evidence' not in data or 'control_id' not in data or 'enhancement' not in data:
            return jsonify({"error": "Invalid input: 'evidence', 'control_id', and 'enhancement' are required."}), 400

        evidence = data['evidence']
        control_id = data['control_id']
        enhancement = data['enhancement']

        # Step 1: Get the 'base_score' and justification from the AI Thinker
        analysis_result = ai_thinker.analyze_control_evidence(
            evidence=evidence,
            control_id=control_id
        )
        base_score = analysis_result.get('base_score', 0)
        justification = analysis_result.get('justification', 'No justification provided.')

        # Step 2: Calculate the 'final_score' using the Score Calculator
        final_score = score_calculator.calculate_control_score(base_score, enhancement)
        
        # Step 3: Return a comprehensive result to the frontend
        return jsonify({
            'justification': justification,
            'base_score': base_score,
            'final_score': final_score
        })

    except Exception as e:
        # Handle any errors that occur during the process
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred during analysis", "details": str(e)}), 500


# The old assessment endpoint can be kept for now or removed later.
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
        report = score_calculator.generate_assessment_report(assessment_data)

        # Return the report as a JSON response
        return jsonify(report)

    except Exception as e:
        # Handle any errors that occur during the process
        app.logger.error(f"An error occurred during assessment: {e}")
        return jsonify({"error": "An error occurred during assessment", "details": str(e)}), 500


if __name__ == '__main__':
    # It's recommended to use a production-ready WSGI server like Gunicorn or Waitress
    # instead of Flask's built-in server for deployment.
    # For Railway, you typically define the start command in a Procfile.
    # Example Procfile: web: gunicorn app:app
    app.run(debug=True, port=int(os.environ.get('PORT', 5001))) 