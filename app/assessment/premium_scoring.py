from app.assessment.premium_questions import PREMIUM_ASSESSMENT_QUESTIONS, CATEGORY_DESCRIPTIONS

def calculate_category_scores(responses):
    """Calculate scores for each personality category"""
    # Group responses by category
    category_responses = {}
    for response in responses:
        question = next((q for q in PREMIUM_ASSESSMENT_QUESTIONS if q['id'] == response.question_id), None)
        if question:
            category = question['category']
            if category not in category_responses:
                category_responses[category] = []
            category_responses[category].append({
                'question': question,
                'answer': response.answer
            })

    # Calculate scores for each category
    category_scores = {}
    for category, responses_list in category_responses.items():
        total_score = 0
        max_possible = len(responses_list) * 5  # Likert scale 1-5

        for resp in responses_list:
            score = int(resp['answer'])
            # Handle reverse-scored questions
            if resp['question'].get('reverse_scored', False):
                score = 6 - score  # Reverse 1-5 scale
            total_score += score

        category_scores[category] = {
            'raw_score': total_score,
            'percentage': round((total_score / max_possible) * 100, 1),
            'max_possible': max_possible,
            'question_count': len(responses_list)
        }

    return category_scores

def get_category_interpretation(category, percentage):
    """Get interpretation for a category score"""
    if percentage >= 80:
        level = "Very High"
        description = "Exceptionally strong in this area"
    elif percentage >= 65:
        level = "High"
        description = "Strong capability in this area"
    elif percentage >= 50:
        level = "Moderate"
        description = "Balanced approach in this area"
    elif percentage >= 35:
        level = "Low"
        description = "Area for potential development"
    else:
        level = "Very Low"
        description = "Significant opportunity for growth"

    return {
        'level': level,
        'description': description
    }

def generate_personality_insights(category_scores):
    """Generate personality insights based on category scores"""
    insights = {}

    # Find highest and lowest scoring categories
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1]['percentage'], reverse=True)
    highest_categories = [cat for cat, score in sorted_categories[:3]]
    lowest_categories = [cat for cat, score in sorted_categories[-3:]]

    # Generate strengths
    strengths = []
    for category in highest_categories:
        score = category_scores[category]
        if score['percentage'] >= 65:
            cat_desc = CATEGORY_DESCRIPTIONS[category]
            strengths.append(f"Strong {cat_desc['name']} - {cat_desc['description']}")

    # Generate growth areas
    growth_areas = []
    for category in lowest_categories:
        score = category_scores[category]
        if score['percentage'] < 50:
            cat_desc = CATEGORY_DESCRIPTIONS[category]
            growth_areas.append(f"{cat_desc['name']} development - {cat_desc['description']}")

    # Generate overall insights
    overall_score = sum(score['percentage'] for score in category_scores.values()) / len(category_scores)

    insights['overall_score'] = round(overall_score, 1)
    insights['strengths'] = strengths[:5]  # Top 5 strengths
    insights['growth_areas'] = growth_areas[:3]  # Top 3 growth areas

    return insights

def generate_recommendations(category_scores):
    """Generate personalized recommendations based on scores"""
    recommendations = []

    # Big Five recommendations
    if category_scores.get('openness', {}).get('percentage', 0) < 50:
        recommendations.append("Seek out new experiences and learning opportunities to develop intellectual curiosity")

    if category_scores.get('conscientiousness', {}).get('percentage', 0) < 50:
        recommendations.append("Develop better planning and organizational systems to improve task completion")

    if category_scores.get('extraversion', {}).get('percentage', 0) < 50:
        recommendations.append("Practice engaging in social situations to build confidence in group settings")

    if category_scores.get('agreeableness', {}).get('percentage', 0) < 50:
        recommendations.append("Work on active listening and empathy skills to improve relationships")

    if category_scores.get('neuroticism', {}).get('percentage', 0) > 65:  # High neuroticism means low emotional stability
        recommendations.append("Develop stress management and emotional regulation techniques")

    # Professional skills recommendations
    if category_scores.get('emotional_intelligence', {}).get('percentage', 0) < 60:
        recommendations.append("Practice mindfulness and emotional awareness to enhance EQ")

    if category_scores.get('leadership', {}).get('percentage', 0) < 60:
        recommendations.append("Seek leadership opportunities and mentorship to develop influence skills")

    if category_scores.get('resilience', {}).get('percentage', 0) < 60:
        recommendations.append("Build resilience through challenging experiences and reflection")

    if category_scores.get('decision_making', {}).get('percentage', 0) < 60:
        recommendations.append("Practice structured decision-making frameworks and seek diverse perspectives")

    if category_scores.get('innovation', {}).get('percentage', 0) < 60:
        recommendations.append("Engage in creative activities and cross-functional collaboration")

    return recommendations[:6]  # Return top 6 recommendations

def generate_comprehensive_report(responses):
    """Generate a comprehensive personality assessment report"""
    category_scores = calculate_category_scores(responses)
    insights = generate_personality_insights(category_scores)
    recommendations = generate_recommendations(category_scores)

    # Build HTML report
    report_content = f"""
    <div class="comprehensive-report">
        <h2>Comprehensive Psychometric Assessment Results</h2>

        <div class="alert alert-info mb-4">
            <h3>Overall Personality Score: {insights['overall_score']}%</h3>
            <p>This score represents your overall psychological profile across multiple dimensions.</p>
        </div>

        <div class="row">
            <div class="col-md-6">
                <h3>Category Breakdown</h3>
                <div class="category-scores">
    """

    # Add category scores
    for category, score in category_scores.items():
        cat_desc = CATEGORY_DESCRIPTIONS[category]
        interpretation = get_category_interpretation(category, score['percentage'])

        # Determine progress bar color
        if score['percentage'] >= 70:
            bar_color = "success"
        elif score['percentage'] >= 50:
            bar_color = "warning"
        else:
            bar_color = "danger"

        report_content += f"""
                    <div class="category-item mb-3">
                        <h5>{cat_desc['name']}</h5>
                        <div class="progress mb-2">
                            <div class="progress-bar bg-{bar_color}" role="progressbar"
                                 style="width: {score['percentage']}%"
                                 aria-valuenow="{score['percentage']}"
                                 aria-valuemin="0" aria-valuemax="100">
                                {score['percentage']}%
                            </div>
                        </div>
                        <p class="small"><strong>{interpretation['level']}:</strong> {interpretation['description']}</p>
                        <p class="small text-muted">{cat_desc['description']}</p>
                    </div>
        """

    report_content += """
                </div>
            </div>

            <div class="col-md-6">
                <h3>Key Insights</h3>
    """

    # Add strengths
    if insights['strengths']:
        report_content += """
                <h4>Your Strengths:</h4>
                <ul class="list-group list-group-flush mb-3">
        """
        for strength in insights['strengths']:
            report_content += f'<li class="list-group-item">{strength}</li>'
        report_content += "</ul>"

    # Add growth areas
    if insights['growth_areas']:
        report_content += """
                <h4>Growth Opportunities:</h4>
                <ul class="list-group list-group-flush mb-3">
        """
        for area in insights['growth_areas']:
            report_content += f'<li class="list-group-item">{area}</li>'
        report_content += "</ul>"

    report_content += """
            </div>
        </div>

        <div class="recommendations mt-4">
            <h3>Personalized Development Recommendations</h3>
            <div class="row">
    """

    # Add recommendations in cards
    for i, rec in enumerate(recommendations):
        if i % 2 == 0:
            report_content += '<div class="col-md-6">'

        report_content += f"""
                <div class="card mb-3">
                    <div class="card-body">
                        <p class="card-text">{rec}</p>
                    </div>
                </div>
        """

        if i % 2 == 1 or i == len(recommendations) - 1:
            report_content += '</div>'

    report_content += """
            </div>
        </div>

        <div class="detailed-analysis mt-4">
            <h3>Detailed Category Analysis</h3>
            <div class="accordion" id="categoryAccordion">
    """

    # Add detailed category analysis
    for i, (category, score) in enumerate(category_scores.items()):
        cat_desc = CATEGORY_DESCRIPTIONS[category]
        interpretation = get_category_interpretation(category, score['percentage'])

        report_content += f"""
                <div class="accordion-item">
                    <h2 class="accordion-header" id="heading{i}">
                        <button class="accordion-button collapsed" type="button"
                                data-bs-toggle="collapse" data-bs-target="#collapse{i}"
                                aria-expanded="false" aria-controls="collapse{i}">
                            {cat_desc['name']} - {score['percentage']}% ({interpretation['level']})
                        </button>
                    </h2>
                    <div id="collapse{i}" class="accordion-collapse collapse"
                         aria-labelledby="heading{i}" data-bs-parent="#categoryAccordion">
                        <div class="accordion-body">
                            <p><strong>Score:</strong> {score['raw_score']}/{score['max_possible']} ({score['percentage']}%)</p>
                            <p><strong>Assessment:</strong> {interpretation['description']}</p>
                            <p><strong>Category Description:</strong> {cat_desc['description']}</p>
                            <p><strong>Questions Answered:</strong> {score['question_count']}</p>
                        </div>
                    </div>
                </div>
        """

    report_content += """
            </div>
        </div>

        <div class="report-footer mt-4">
            <p class="text-muted">
                <small>This comprehensive assessment evaluated your personality across multiple psychological dimensions.
                The results provide insights into your behavioral tendencies, strengths, and areas for development.
                Remember that personality is complex and multifaceted - these results represent one perspective
                on your psychological profile.</small>
            </p>
        </div>
    </div>
    """

    return report_content