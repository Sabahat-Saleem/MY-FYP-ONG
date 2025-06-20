from django.utils.timezone import now
from rapidfuzz import fuzz
from .models import Location, Event, TravelTip, TravelSchedule, ScheduleEntry

FUZZY_THRESHOLD = 60  # Adjust threshold for match sensitivity (0-100)

def fuzzy_score(text, keywords):
    """Calculate max fuzzy match score between text and list of keywords."""
    print("DEBUG - fuzzy_score received text:", text)  # 🐞 log the input

    try:
        text = str(text).lower()
    except Exception as e:
        print("ERROR converting text to lowercase:", e)  # Log the error
        raise  # Re-raise for full traceback

    max_score = 0
    for keyword in keywords:
        score = fuzz.partial_ratio(keyword.lower(), text)
        if score > max_score:
            max_score = score
    return max_score

def get_recommendations(user):
    # Base filtered queries
    base_locations = Location.objects.filter(season=user.preferred_season)
    base_events = Event.objects.filter(
        season=user.preferred_season,
        travel_type=user.preferred_travel_type,
        date__gte=now().date()
    )
    base_tips = TravelTip.objects.filter(
        season=user.preferred_season,
        travel_type=user.preferred_travel_type
    )

    # User interests keywords
    user_interests = user.useractivity_set.values_list('interest__name', flat=True)
    user_interests_list = list(user_interests)

    # Score locations by fuzzy matching activities to interests
    scored_locations = []
    for loc in base_locations:
        score = fuzzy_score(loc.activities, user_interests_list)
        scored_locations.append((score, loc))
    scored_locations.sort(key=lambda x: x[0], reverse=True)
    recommended_locations = [loc for score, loc in scored_locations if score >= FUZZY_THRESHOLD] or list(base_locations)

    # Score events by fuzzy matching name + description
    scored_events = []
    for ev in base_events:
        combined_text = f"{ev.name} {ev.description}"
        score = fuzzy_score(combined_text, user_interests_list)
        scored_events.append((score, ev))
    scored_events.sort(key=lambda x: x[0], reverse=True)
    recommended_events = [ev for score, ev in scored_events if score >= FUZZY_THRESHOLD] or list(base_events)

    # Score tips by fuzzy matching title + content
    scored_tips = []
    for tip in base_tips:
        combined_text = f"{tip.title} {tip.content}"
        score = fuzzy_score(combined_text, user_interests_list)
        scored_tips.append((score, tip))
    scored_tips.sort(key=lambda x: x[0], reverse=True)
    recommended_tips = [tip for score, tip in scored_tips if score >= FUZZY_THRESHOLD] or list(base_tips)

    # Upcoming schedules and entries for user (no scoring)
    schedules = TravelSchedule.objects.filter(user=user, end_date__gte=now().date())
    schedule_entries = ScheduleEntry.objects.filter(schedule__in=schedules)

    return {
        'locations': recommended_locations,
        'events': recommended_events,
        'tips': recommended_tips,
        'schedule_entries': schedule_entries,
    }
