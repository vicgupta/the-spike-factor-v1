def calculate_spike_factor(responses):
    """Calculate spike factor based on assessment responses"""

    # Sample scoring algorithm - can be enhanced based on psychological models
    total_score = 0
    max_score = len(responses) * 5  # Assuming 5-point scale

    for response in responses:
        # Convert text response to numerical score
        answer = response.answer.lower()
        if 'strongly agree' in answer or answer == '5':
            score = 5
        elif 'agree' in answer or answer == '4':
            score = 4
        elif 'neutral' in answer or answer == '3':
            score = 3
        elif 'disagree' in answer or answer == '2':
            score = 2
        elif 'strongly disagree' in answer or answer == '1':
            score = 1
        else:
            score = 3  # Default neutral

        total_score += score

    # Calculate percentage
    spike_factor = (total_score / max_score) * 100

    return round(spike_factor, 1)

def generate_personality_insights(spike_factor, responses):
    """Generate personality insights based on spike factor"""

    insights = {
        'spike_factor': spike_factor,
        'category': '',
        'strengths': [],
        'growth_areas': [],
        'recommendations': []
    }

    if spike_factor >= 80:
        insights['category'] = 'High Spike Factor'
        insights['strengths'] = [
            'Strong leadership potential',
            'High energy and motivation',
            'Excellent at handling challenges'
        ]
        insights['growth_areas'] = [
            'May benefit from patience in team settings',
            'Consider work-life balance'
        ]
        insights['recommendations'] = [
            'Seek leadership roles',
            'Practice mindfulness techniques',
            'Mentor others in your field'
        ]
    elif spike_factor >= 60:
        insights['category'] = 'Moderate Spike Factor'
        insights['strengths'] = [
            'Balanced approach to challenges',
            'Good team collaboration skills',
            'Steady performance under pressure'
        ]
        insights['growth_areas'] = [
            'Could push boundaries more',
            'Develop confidence in decision-making'
        ]
        insights['recommendations'] = [
            'Take on stretch assignments',
            'Seek feedback regularly',
            'Build network of mentors'
        ]
    else:
        insights['category'] = 'Developing Spike Factor'
        insights['strengths'] = [
            'Thoughtful and deliberate approach',
            'Strong attention to detail',
            'Collaborative team member'
        ]
        insights['growth_areas'] = [
            'Build confidence in abilities',
            'Practice assertiveness',
            'Embrace calculated risks'
        ]
        insights['recommendations'] = [
            'Start with small challenges',
            'Celebrate small wins',
            'Seek supportive environments'
        ]

    return insights