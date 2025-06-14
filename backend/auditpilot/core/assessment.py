"""
Core assessment module for AuditPilot AI Scorecard
"""
from typing import Dict, List, Tuple, Optional
import datetime
import json

class AISecurityAssessment:
    def __init__(self):
        # Control family weights from ARC-AMPE framework
        self.control_families = {
            'AC': {'weight': 0.08, 'name': 'Access Control'},
            'AU': {'weight': 0.07, 'name': 'Audit and Accountability'},
            'AT': {'weight': 0.03, 'name': 'Awareness and Training'},
            'CA': {'weight': 0.06, 'name': 'Assessment, Authorization, and Monitoring'},
            'CM': {'weight': 0.05, 'name': 'Configuration Management'},
            'CP': {'weight': 0.04, 'name': 'Contingency Planning'},
            'IA': {'weight': 0.08, 'name': 'Identification and Authentication'},
            'IR': {'weight': 0.06, 'name': 'Incident Response'},
            'MA': {'weight': 0.03, 'name': 'Maintenance'},
            'MP': {'weight': 0.04, 'name': 'Media Protection'},
            'PE': {'weight': 0.03, 'name': 'Physical and Environmental Protection'},
            'PL': {'weight': 0.04, 'name': 'Planning'},
            'PS': {'weight': 0.04, 'name': 'Personnel Security'},
            'RA': {'weight': 0.06, 'name': 'Risk Assessment'},
            'SA': {'weight': 0.04, 'name': 'System and Services Acquisition'},
            'SC': {'weight': 0.09, 'name': 'System and Communications Protection'},
            'SI': {'weight': 0.07, 'name': 'System and Information Integrity'}
        }

        # Enhancement multipliers for AI capabilities
        self.enhancement_multipliers = {
            'none': 1.0,
            'moderate': 1.1,
            'significant': 1.25,
            'transformational': 1.5
        }

        # Maturity level thresholds
        self.maturity_levels = {
            'basic': (0, 40),
            'developing': (41, 60),
            'mature': (61, 80),
            'advanced': (81, 100)
        }

    def calculate_control_score(self, base_score: int, enhancement_level: str) -> float:
        """Calculate enhanced control score with AI agent multiplier"""
        multiplier = self.enhancement_multipliers.get(enhancement_level, 1.0)
        return min(base_score * multiplier, 100)  # Cap at 100

    def calculate_family_score(self, control_scores: List[Tuple[int, str]]) -> float:
        """Calculate weighted family score"""
        if not control_scores:
            return 0
        total_score = 0
        for base_score, enhancement in control_scores:
            total_score += self.calculate_control_score(base_score, enhancement)
        return total_score / len(control_scores)

    def calculate_overall_score(self, family_scores: Dict[str, float]) -> float:
        """Calculate weighted overall assessment score"""
        total_weighted_score = 0
        for family_id, score in family_scores.items():
            if family_id in self.control_families:
                weight = self.control_families[family_id]['weight']
                total_weighted_score += score * weight
        return total_weighted_score

    def determine_maturity_level(self, overall_score: float) -> str:
        """Determine organizational maturity level"""
        for level, (min_score, max_score) in self.maturity_levels.items():
            if min_score <= overall_score <= max_score:
                return level
        return 'unknown'

    def generate_recommendations(self, family_scores: Dict[str, float], overall_score: float) -> List[str]:
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        # Identify low-scoring families
        low_scoring_families = [
            (family_id, score) for family_id, score in family_scores.items()
            if score < 60
        ]
        
        if low_scoring_families:
            recommendations.append("Priority focus areas identified:")
            for family_id, score in sorted(low_scoring_families, key=lambda x: x[1]):
                family_name = self.control_families[family_id]['name']
                recommendations.append(
                    f"- {family_name} ({family_id}): {score:.1f}% - Requires immediate attention"
                )

        # Maturity-based recommendations
        if overall_score < 40:
            recommendations.extend([
                "Critical: Implement foundational security controls immediately",
                "Focus on quantum-resistant cryptography deployment",
                "Establish basic explainable AI capabilities"
            ])
        elif overall_score < 60:
            recommendations.extend([
                "Optimize existing controls and enhance AI agent capabilities",
                "Implement homomorphic encryption for privacy protection",
                "Activate self-healing policy synthesis engine"
            ])
        elif overall_score < 80:
            recommendations.extend([
                "Focus on continuous improvement and optimization",
                "Enhance automated monitoring and response capabilities",
                "Implement advanced threat detection and analysis"
            ])
        else:
            recommendations.extend([
                "Maintain leadership position through innovation",
                "Contribute to industry best practices and standards",
                "Prepare for next-generation regulatory requirements"
            ])

        return recommendations

    def generate_assessment_report(self, assessment_data: Dict) -> Dict:
        """Generate comprehensive assessment report"""
        family_scores = {}
        for family_id, controls in assessment_data.items():
            if family_id in self.control_families:
                control_scores = [(c['base_score'], c['enhancement']) 
                                for c in controls]
                family_scores[family_id] = self.calculate_family_score(control_scores)

        overall_score = self.calculate_overall_score(family_scores)
        maturity_level = self.determine_maturity_level(overall_score)

        return {
            'assessment_date': datetime.datetime.now().isoformat(),
            'overall_score': round(overall_score, 2),
            'maturity_level': maturity_level,
            'family_scores': {k: round(v, 2) for k, v in family_scores.items()},
            'recommendations': self.generate_recommendations(family_scores, overall_score)
        } 