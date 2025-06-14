"""
Example usage of AuditPilot AI Compliance Assessment
"""
from auditpilot.core.ai_analyzer import AIComplianceAnalyzer
from auditpilot.core.evidence_collector import EvidenceCollector
import json
from pprint import pprint

def run_example_assessment():
    # Initialize components
    analyzer = AIComplianceAnalyzer()
    collector = EvidenceCollector()
    
    # Example input data for AC-1 (Access Control Policy)
    example_inputs = {
        'documentation': {
            'has_policies': True,
            'policy_details': {
                'completeness': 0.8,
                'accuracy': 0.9,
                'currency': 0.7
            },
            'has_procedures': True,
            'procedure_details': {
                'completeness': 0.7,
                'accuracy': 0.8,
                'currency': 0.6
            },
            'has_guidelines': True,
            'guideline_details': {
                'completeness': 0.6,
                'accuracy': 0.7,
                'currency': 0.8
            }
        },
        'implementation': {
            'technical': {
                'effectiveness': 0.75,
                'validation': True,
                'testing': True
            },
            'administrative': {
                'effectiveness': 0.8,
                'validation': True,
                'testing': True
            },
            'physical': {
                'effectiveness': 0.7,
                'validation': True,
                'testing': False
            },
            'documented_processes': 0.8,
            'regular_testing': 0.7,
            'continuous_monitoring': 0.6,
            'improvement_process': 0.7,
            'automation_level': 0.5
        },
        'risk_assessment': {
            'threat_level': 0.3,
            'vulnerability_score': 0.2,
            'impact_rating': 0.4,
            'last_assessment': '2023-11-23',
            'assessor': 'Security Team'
        },
        'automation': {
            'monitoring_automation': 0.6,
            'response_automation': 0.5,
            'reporting_automation': 0.7,
            'update_automation': 0.4,
            'validation_automation': 0.5
        },
        'monitoring': {
            'monitoring_coverage': 0.7,
            'alerting_effectiveness': 0.6,
            'response_time_score': 0.8
        },
        'incidents': {
            'incidents': [
                {
                    'date': '2023-10-15',
                    'severity': 'low',
                    'description': 'Failed login attempts'
                },
                {
                    'date': '2023-09-20',
                    'severity': 'medium',
                    'description': 'Unauthorized access attempt'
                }
            ]
        },
        'updates': {
            'update_frequency': 0.8,
            'update_coverage': 0.7,
            'update_validation': 0.6
        }
    }
    
    # Collect and structure evidence
    evidence = collector.collect_control_evidence('AC-1', example_inputs)
    
    # Analyze evidence using AI
    analysis_results = analyzer.analyze_control_evidence(evidence)
    
    # Print results
    print("\n=== AuditPilot AI Compliance Assessment Results ===\n")
    print(f"Control: AC-1 (Access Control Policy)")
    print(f"Compliance Score: {analysis_results['compliance_score']:.2f}%")
    print(f"Confidence Score: {analysis_results['confidence_score']:.2f}%")
    
    print("\nKey Findings:")
    for finding in analysis_results['analysis']['key_findings']:
        print(f"- {finding}")
    
    print("\nRisk Factors:")
    for risk in analysis_results['risk_factors']:
        print(f"- {risk['factor']} (Severity: {risk['severity']})")
        print(f"  Description: {risk['description']}")
    
    print("\nImprovement Recommendations:")
    for improvement in analysis_results['improvement_areas']:
        print(f"\n{improvement['area']} (Priority: {improvement['priority']}):")
        for suggestion in improvement['suggestions']:
            print(f"- {suggestion}")

if __name__ == '__main__':
    run_example_assessment() 