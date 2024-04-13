from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from flask import Flask, jsonify, request
from event_analyzer import EventAnalyzer
from event_file_manager import EventFileManager

router = APIRouter()


@router.get("/events", response_model=List[Event])
async def get_all_events():
    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)



@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):

    # Retrieve parameters from the request query string
    date = request.args.get('date')
    organizer = request.args.get('organizer')
    status = request.args.get('status')
    event_type = request.args.get('event_type')
    
    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Filter events based on the given parameters
    filtered_events = events
    if date:
        filtered_events = [event for event in filtered_events if event.get('date') == date]
    if organizer:
        filtered_events = [event for event in filtered_events if event.get('organizer') == organizer]
    if status:
        filtered_events = [event for event in filtered_events if event.get('status') == status]
    if event_type:
        filtered_events = [event for event in filtered_events if event.get('event_type') == event_type]
    
    return jsonify(filtered_events)




@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):

    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Search for the event with the provided ID
    for event in events:
        if event.get('id') == event_id:
            return jsonify(event)
    
    # If the event with the provided ID does not exist, return a message
    return jsonify({"message": "Event not found"}), 404



@router.post("/events", response_model=Event)
async def create_event(event: Event):

    # Retrieve the new event data from the request
    new_event = request.json
    
    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Check if the event ID already exists
    event_ids = [event.get('id') for event in events]
    if new_event.get('id') in event_ids:
        return jsonify({"message": "Event ID already exists"}), 400
    
    # Add the new event to the list of events
    events.append(new_event)
    
    # Write the updated list of events back to the events file
    EventFileManager.write_events_to_file(events)
    
    return jsonify({"message": "Event created successfully"})



@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    # Retrieve the updated event data from the request
    updated_event = request.json
    
    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Search for the event with the provided ID
    event_found = False
    for event in events:
        if event.get('id') == event_id:
            event_found = True
            # Update the event with the provided ID
            event.update(updated_event)
            break
    
    # If the event with the provided ID is not found, return a message
    if not event_found:
        return jsonify({"message": "Event not found"}), 404
    
    # Write the updated list of events back to the events file
    EventFileManager.write_events_to_file(events)
    
    return jsonify({"message": "Event updated successfully"})



@router.delete("/events/{event_id}")
async def delete_event(event_id: int):

    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Search for the event with the provided ID
    event_found = False
    for event in events:
        if event.get('id') == event_id:
            event_found = True
            # Remove the event with the provided ID
            events.remove(event)
            break
    
    # If the event with the provided ID is not found, return a message
    if not event_found:
        return jsonify({"message": "Event not found"}), 404
    
    # Write the updated list of events back to the events file
    EventFileManager.write_events_to_file(events)
    
    return jsonify({"message": "Event deleted successfully"})



@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    # Utilize EventFileManager class to retrieve all events
    events = EventFileManager.read_events_from_file()
    
    # Initialize EventAnalyzer class
    event_analyzer = EventAnalyzer()
    
    # Get joiners who attended multiple meetings
    joiners_multiple_meetings = event_analyzer.get_joiners_multiple_meetings(events)
    
    if not joiners_multiple_meetings:
        return jsonify({"message": "No joiners attending at least 2 meetings"})
    
    return jsonify(joiners_multiple_meetings)

