# Comprehensive Psychometric Assessment - 84 Questions
# Categories: Big Five Personality Traits, Emotional Intelligence, Leadership, Resilience,
# Motivation, Social Skills, Decision Making, Innovation, and Work Style

PREMIUM_ASSESSMENT_QUESTIONS = [
    # Big Five - Openness to Experience (8 questions)
    {
        'id': 1,
        'category': 'openness',
        'question': 'I enjoy exploring abstract concepts and philosophical ideas.',
        'type': 'likert'
    },
    {
        'id': 2,
        'category': 'openness',
        'question': 'I am always curious about learning how things work.',
        'type': 'likert'
    },
    {
        'id': 3,
        'category': 'openness',
        'question': 'I appreciate art, music, and creative expressions.',
        'type': 'likert'
    },
    {
        'id': 4,
        'category': 'openness',
        'question': 'I prefer routine and predictable environments.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 5,
        'category': 'openness',
        'question': 'I enjoy trying new foods and experiencing different cultures.',
        'type': 'likert'
    },
    {
        'id': 6,
        'category': 'openness',
        'question': 'I often come up with creative solutions to problems.',
        'type': 'likert'
    },
    {
        'id': 7,
        'category': 'openness',
        'question': 'I find imaginative and fantasy stories boring.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 8,
        'category': 'openness',
        'question': 'I seek out intellectual challenges and complex problems.',
        'type': 'likert'
    },

    # Big Five - Conscientiousness (10 questions)
    {
        'id': 9,
        'category': 'conscientiousness',
        'question': 'I always complete tasks I start, even when they become difficult.',
        'type': 'likert'
    },
    {
        'id': 10,
        'category': 'conscientiousness',
        'question': 'I plan my work schedule carefully and stick to it.',
        'type': 'likert'
    },
    {
        'id': 11,
        'category': 'conscientiousness',
        'question': 'I often procrastinate on important tasks.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 12,
        'category': 'conscientiousness',
        'question': 'I pay attention to details and avoid making careless mistakes.',
        'type': 'likert'
    },
    {
        'id': 13,
        'category': 'conscientiousness',
        'question': 'I am reliable and others can count on me to follow through.',
        'type': 'likert'
    },
    {
        'id': 14,
        'category': 'conscientiousness',
        'question': 'I prefer to work spontaneously rather than follow a plan.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 15,
        'category': 'conscientiousness',
        'question': 'I set high standards for myself and work hard to achieve them.',
        'type': 'likert'
    },
    {
        'id': 16,
        'category': 'conscientiousness',
        'question': 'I keep my workspace and belongings well-organized.',
        'type': 'likert'
    },
    {
        'id': 17,
        'category': 'conscientiousness',
        'question': 'I often leave tasks unfinished.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 18,
        'category': 'conscientiousness',
        'question': 'I am disciplined and can resist temptations that interfere with my goals.',
        'type': 'likert'
    },

    # Big Five - Extraversion (10 questions)
    {
        'id': 19,
        'category': 'extraversion',
        'question': 'I feel energized when I am around other people.',
        'type': 'likert'
    },
    {
        'id': 20,
        'category': 'extraversion',
        'question': 'I enjoy being the center of attention in social gatherings.',
        'type': 'likert'
    },
    {
        'id': 21,
        'category': 'extraversion',
        'question': 'I prefer working alone rather than in groups.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 22,
        'category': 'extraversion',
        'question': 'I am talkative and enjoy engaging in conversations.',
        'type': 'likert'
    },
    {
        'id': 23,
        'category': 'extraversion',
        'question': 'I feel comfortable approaching strangers.',
        'type': 'likert'
    },
    {
        'id': 24,
        'category': 'extraversion',
        'question': 'I prefer quiet, low-key social activities.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 25,
        'category': 'extraversion',
        'question': 'I actively seek out leadership opportunities.',
        'type': 'likert'
    },
    {
        'id': 26,
        'category': 'extraversion',
        'question': 'I enjoy lively, stimulating environments.',
        'type': 'likert'
    },
    {
        'id': 27,
        'category': 'extraversion',
        'question': 'I am reserved and quiet in most social situations.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 28,
        'category': 'extraversion',
        'question': 'I find it easy to make new friends.',
        'type': 'likert'
    },

    # Big Five - Agreeableness (8 questions)
    {
        'id': 29,
        'category': 'agreeableness',
        'question': 'I trust people and believe they have good intentions.',
        'type': 'likert'
    },
    {
        'id': 30,
        'category': 'agreeableness',
        'question': 'I am generous and willing to help others even when it costs me.',
        'type': 'likert'
    },
    {
        'id': 31,
        'category': 'agreeableness',
        'question': 'I often find myself in arguments with others.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 32,
        'category': 'agreeableness',
        'question': 'I am sympathetic and concerned about others\' feelings.',
        'type': 'likert'
    },
    {
        'id': 33,
        'category': 'agreeableness',
        'question': 'I prefer to compete rather than cooperate.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 34,
        'category': 'agreeableness',
        'question': 'I forgive others easily and don\'t hold grudges.',
        'type': 'likert'
    },
    {
        'id': 35,
        'category': 'agreeableness',
        'question': 'I am suspicious of others\' motives.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 36,
        'category': 'agreeableness',
        'question': 'I enjoy working collaboratively to achieve common goals.',
        'type': 'likert'
    },

    # Big Five - Neuroticism (8 questions)
    {
        'id': 37,
        'category': 'neuroticism',
        'question': 'I often feel anxious and worried about future events.',
        'type': 'likert'
    },
    {
        'id': 38,
        'category': 'neuroticism',
        'question': 'I remain calm and composed under pressure.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 39,
        'category': 'neuroticism',
        'question': 'My mood changes frequently throughout the day.',
        'type': 'likert'
    },
    {
        'id': 40,
        'category': 'neuroticism',
        'question': 'I recover quickly from stressful situations.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 41,
        'category': 'neuroticism',
        'question': 'I often feel overwhelmed by daily responsibilities.',
        'type': 'likert'
    },
    {
        'id': 42,
        'category': 'neuroticism',
        'question': 'I am generally optimistic about the future.',
        'type': 'likert',
        'reverse_scored': True
    },
    {
        'id': 43,
        'category': 'neuroticism',
        'question': 'I tend to worry about things that might go wrong.',
        'type': 'likert'
    },
    {
        'id': 44,
        'category': 'neuroticism',
        'question': 'I feel emotionally stable and even-tempered.',
        'type': 'likert',
        'reverse_scored': True
    },

    # Emotional Intelligence (10 questions)
    {
        'id': 45,
        'category': 'emotional_intelligence',
        'question': 'I can accurately identify my own emotions as they occur.',
        'type': 'likert'
    },
    {
        'id': 46,
        'category': 'emotional_intelligence',
        'question': 'I understand what triggers my emotional responses.',
        'type': 'likert'
    },
    {
        'id': 47,
        'category': 'emotional_intelligence',
        'question': 'I can easily read other people\'s emotional states.',
        'type': 'likert'
    },
    {
        'id': 48,
        'category': 'emotional_intelligence',
        'question': 'I manage my emotions effectively in stressful situations.',
        'type': 'likert'
    },
    {
        'id': 49,
        'category': 'emotional_intelligence',
        'question': 'I can motivate myself to persist through difficult tasks.',
        'type': 'likert'
    },
    {
        'id': 50,
        'category': 'emotional_intelligence',
        'question': 'I am skilled at helping others manage their emotions.',
        'type': 'likert'
    },
    {
        'id': 51,
        'category': 'emotional_intelligence',
        'question': 'I use my emotions to guide my decision-making.',
        'type': 'likert'
    },
    {
        'id': 52,
        'category': 'emotional_intelligence',
        'question': 'I can adapt my communication style based on others\' emotional needs.',
        'type': 'likert'
    },
    {
        'id': 53,
        'category': 'emotional_intelligence',
        'question': 'I recognize when my emotions might cloud my judgment.',
        'type': 'likert'
    },
    {
        'id': 54,
        'category': 'emotional_intelligence',
        'question': 'I can remain empathetic even when I disagree with someone.',
        'type': 'likert'
    },

    # Leadership & Influence (8 questions)
    {
        'id': 55,
        'category': 'leadership',
        'question': 'I naturally take charge in group situations.',
        'type': 'likert'
    },
    {
        'id': 56,
        'category': 'leadership',
        'question': 'I can inspire others to work toward a common vision.',
        'type': 'likert'
    },
    {
        'id': 57,
        'category': 'leadership',
        'question': 'I delegate tasks effectively and trust others to deliver.',
        'type': 'likert'
    },
    {
        'id': 58,
        'category': 'leadership',
        'question': 'I am comfortable making difficult decisions that affect others.',
        'type': 'likert'
    },
    {
        'id': 59,
        'category': 'leadership',
        'question': 'I provide constructive feedback to help others improve.',
        'type': 'likert'
    },
    {
        'id': 60,
        'category': 'leadership',
        'question': 'I can influence others without using formal authority.',
        'type': 'likert'
    },
    {
        'id': 61,
        'category': 'leadership',
        'question': 'I take responsibility for team failures as well as successes.',
        'type': 'likert'
    },
    {
        'id': 62,
        'category': 'leadership',
        'question': 'I adapt my leadership style to different people and situations.',
        'type': 'likert'
    },

    # Resilience & Adaptability (8 questions)
    {
        'id': 63,
        'category': 'resilience',
        'question': 'I bounce back quickly from setbacks and failures.',
        'type': 'likert'
    },
    {
        'id': 64,
        'category': 'resilience',
        'question': 'I view challenges as opportunities for growth.',
        'type': 'likert'
    },
    {
        'id': 65,
        'category': 'resilience',
        'question': 'I maintain my performance during times of uncertainty.',
        'type': 'likert'
    },
    {
        'id': 66,
        'category': 'resilience',
        'question': 'I adapt quickly to changes in my environment.',
        'type': 'likert'
    },
    {
        'id': 67,
        'category': 'resilience',
        'question': 'I learn from my mistakes and apply those lessons.',
        'type': 'likert'
    },
    {
        'id': 68,
        'category': 'resilience',
        'question': 'I can maintain a positive attitude during difficult times.',
        'type': 'likert'
    },
    {
        'id': 69,
        'category': 'resilience',
        'question': 'I seek support from others when facing major challenges.',
        'type': 'likert'
    },
    {
        'id': 70,
        'category': 'resilience',
        'question': 'I persist through obstacles even when progress is slow.',
        'type': 'likert'
    },

    # Decision Making & Risk (8 questions)
    {
        'id': 71,
        'category': 'decision_making',
        'question': 'I am comfortable making decisions with incomplete information.',
        'type': 'likert'
    },
    {
        'id': 72,
        'category': 'decision_making',
        'question': 'I consider multiple perspectives before making important decisions.',
        'type': 'likert'
    },
    {
        'id': 73,
        'category': 'decision_making',
        'question': 'I am willing to take calculated risks to achieve my goals.',
        'type': 'likert'
    },
    {
        'id': 74,
        'category': 'decision_making',
        'question': 'I analyze potential consequences thoroughly before acting.',
        'type': 'likert'
    },
    {
        'id': 75,
        'category': 'decision_making',
        'question': 'I trust my intuition when making quick decisions.',
        'type': 'likert'
    },
    {
        'id': 76,
        'category': 'decision_making',
        'question': 'I seek input from others before making major decisions.',
        'type': 'likert'
    },
    {
        'id': 77,
        'category': 'decision_making',
        'question': 'I am decisive and avoid excessive deliberation.',
        'type': 'likert'
    },
    {
        'id': 78,
        'category': 'decision_making',
        'question': 'I take responsibility for the outcomes of my decisions.',
        'type': 'likert'
    },

    # Innovation & Creativity (6 questions)
    {
        'id': 79,
        'category': 'innovation',
        'question': 'I often generate original ideas and solutions.',
        'type': 'likert'
    },
    {
        'id': 80,
        'category': 'innovation',
        'question': 'I challenge conventional ways of doing things.',
        'type': 'likert'
    },
    {
        'id': 81,
        'category': 'innovation',
        'question': 'I am excited by the possibility of creating something new.',
        'type': 'likert'
    },
    {
        'id': 82,
        'category': 'innovation',
        'question': 'I can see connections between seemingly unrelated concepts.',
        'type': 'likert'
    },
    {
        'id': 83,
        'category': 'innovation',
        'question': 'I experiment with new approaches even if they might fail.',
        'type': 'likert'
    },
    {
        'id': 84,
        'category': 'innovation',
        'question': 'I encourage others to think outside the box.',
        'type': 'likert'
    }
]

# Category descriptions for scoring and reporting
CATEGORY_DESCRIPTIONS = {
    'openness': {
        'name': 'Openness to Experience',
        'description': 'Reflects curiosity, creativity, and willingness to try new experiences.'
    },
    'conscientiousness': {
        'name': 'Conscientiousness',
        'description': 'Measures organization, discipline, and goal-oriented behavior.'
    },
    'extraversion': {
        'name': 'Extraversion',
        'description': 'Indicates energy from social interaction and outgoing behavior.'
    },
    'agreeableness': {
        'name': 'Agreeableness',
        'description': 'Reflects cooperation, trust, and concern for others.'
    },
    'neuroticism': {
        'name': 'Emotional Stability',
        'description': 'Measures emotional stability and stress management.'
    },
    'emotional_intelligence': {
        'name': 'Emotional Intelligence',
        'description': 'Ability to understand and manage emotions in self and others.'
    },
    'leadership': {
        'name': 'Leadership & Influence',
        'description': 'Capacity to guide, motivate, and influence others effectively.'
    },
    'resilience': {
        'name': 'Resilience & Adaptability',
        'description': 'Ability to bounce back from setbacks and adapt to change.'
    },
    'decision_making': {
        'name': 'Decision Making & Risk',
        'description': 'Effectiveness in making decisions and managing risk.'
    },
    'innovation': {
        'name': 'Innovation & Creativity',
        'description': 'Capacity for creative thinking and innovative problem-solving.'
    }
}