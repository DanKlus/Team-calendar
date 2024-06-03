from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String, Boolean

DATABASE_URL = "sqlite:///events.db"

app = Flask(__name__)

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    start = Column(String, nullable=False)
    backgroundColor = Column(String, nullable=False)
    borderColor = Column(String, nullable=False)
    allDay = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)  # Add name column
    status = Column(String, nullable=False)  # Add status column

Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_event', methods=['POST'])
def save_event():
    event_data = request.get_json()
    db = SessionLocal()
    event = Event(
        title=event_data['title'],
        start=event_data['start'],
        backgroundColor=event_data['backgroundColor'],
        borderColor=event_data['borderColor'],
        allDay=event_data['allDay'],
        name=event_data['name'],  # Save name
        status=event_data['status']  # Save status
    )
    db.add(event)
    db.commit()
    db.refresh(event)  # Refresh to get the new ID
    db.close()
    return jsonify({'status': 'success', 'event': {
        'id': event.id,
        'title': event.title,
        'start': event.start,
        'backgroundColor': event.backgroundColor,
        'borderColor': event.borderColor,
        'allDay': event.allDay,
        'name': event.name,
        'status': event.status
    }}), 200

@app.route('/update_event', methods=['POST'])
def update_event():
    event_data = request.get_json()
    db = SessionLocal()
    event = db.query(Event).filter(Event.id == event_data['id']).first()
    if event:
        event.title = event_data['title']
        event.start = event_data['start']
        event.backgroundColor = event_data['backgroundColor']
        event.borderColor = event_data['borderColor']
        event.allDay = event_data['allDay']
        event.name = event_data['name']
        event.status = event_data['status']
        db.commit()
    db.close()
    return jsonify({'status': 'success', 'event': event_data}), 200

@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_data = request.get_json()
    db = SessionLocal()
    db.query(Event).filter(Event.id == event_data['id']).delete()
    db.commit()
    db.close()
    return jsonify({'status': 'success'}), 200

@app.route('/get_events', methods=['GET'])
def get_events():
    db = SessionLocal()
    events = db.query(Event).all()
    events_list = [{'id': event.id, 'title': event.title, 'start': event.start, 'backgroundColor': event.backgroundColor, 'borderColor': event.borderColor, 'allDay': event.allDay, 'name': event.name, 'status': event.status} for event in events]
    db.close()
    return jsonify(events_list)

if __name__ == '__main__':
    app.run(debug=True)
