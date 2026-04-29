# NEET Spaced Repetition Tracker

## 🎯 Overview

A sophisticated web application designed to help NEET aspirants master their preparation through adaptive spaced repetition learning. This system intelligently schedules revision sessions based on individual performance, ensuring optimal retention and long-term memory formation.

## 🌟 Key Features

### 📚 Adaptive Learning Algorithm
- **Performance-based scheduling**: Revision intervals adjust based on difficulty ratings
- **Infinite revision cycle**: System continues indefinitely without fixed limits
- **Smart interval progression**: Uses scientifically-backed base intervals [1, 3, 7, 14, 21, 30, 60] days
- **Dynamic difficulty handling**: Easy/Medium/Hard responses trigger different interval calculations

### 📖 Topic Management
- **Quick topic addition**: Simple interface to add new study topics
- **Automatic scheduling**: New topics start with 1-day initial interval
- **Topic deletion**: Remove topics along with their revision history

### 📊 Dashboard Analytics
- **Today's revisions**: Clear view of pending tasks for current day
- **Upcoming schedule**: Preview of next revision sessions
- **Real-time statistics**: Track daily and upcoming task counts
- **Visual indicators**: Color-coded cards for today vs upcoming revisions

### 🎨 User Experience
- **Clean, modern interface**: Gradient backgrounds and smooth animations
- **Responsive design**: Works seamlessly on desktop and mobile devices
- **Intuitive controls**: Easy/Medium/Hard buttons for quick feedback
- **Visual feedback**: Hover effects and transitions for better interaction

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Powerful ORM for database operations
- **SQLite**: Lightweight, file-based database
- **Uvicorn**: ASGI server for production deployment

### Frontend
- **Jinja2 Templates**: Server-side rendering with template inheritance
- **Custom CSS**: Modern styling with gradients and animations
- **HTML5**: Semantic markup for accessibility

### Database Design
```sql
topics:
- id (Primary Key)
- name (Unique)

revisions:
- id (Primary Key)
- topic_id (Foreign Key)
- next_revision_date
- interval_level
- last_interval_days
- status (pending/done)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download the Project
```bash
# Navigate to your desired directory
cd path/to/your/projects

# If using git (if available)
git clone <repository-url> neet-tracker
cd neet-tracker

# Or simply extract the project files
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
uvicorn main:app --reload
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://localhost:8000
```

## 📁 Project Structure

```
NEET/
├── main.py              # FastAPI application with routes and business logic
├── models.py            # SQLAlchemy database models
├── database.py          # Database configuration and session management
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── templates/
│   └── index.html      # Main dashboard template
└── static/
    └── style.css       # Custom styling
```

## 🔧 How It Works

### Spaced Repetition Algorithm

The system uses an adaptive algorithm that adjusts revision intervals based on user performance:

1. **Base Intervals**: [1, 3, 7, 14, 21, 30, 60] days
2. **Easy Response**: 
   - Within base intervals: Move to next level
   - Beyond base intervals: Multiply current interval by 2.5
3. **Medium Response**:
   - Within base intervals: Move to next level  
   - Beyond base intervals: Multiply current interval by 1.5
4. **Hard Response**: Reset to level 0 with 1-day interval

### Workflow

1. **Add Topic**: Create new study topics with automatic initial scheduling
2. **Daily Review**: Complete scheduled revisions using difficulty buttons
3. **Adaptive Scheduling**: System automatically calculates next revision dates
4. **Track Progress**: Monitor today's tasks and upcoming schedule

## 🎯 Usage Guide

### Adding Topics
1. Enter topic name in the "Add New Topic" form
2. Click "Add Topic" button
3. System automatically schedules first revision for tomorrow

### Completing Revisions
1. Find topics in "Today's Revisions" section
2. Choose difficulty level: Easy, Medium, or Hard
3. System updates next revision date based on your response

### Managing Topics
1. Use "Delete" button to remove topics
2. All associated revision history is automatically cleaned up

### Viewing Schedule
1. "Today's Revisions" shows pending tasks for current day
2. "Upcoming Revisions" displays next 10 scheduled sessions
3. Statistics section provides task count overview

## 🔮 Future Enhancements

### Planned Features
- **User Authentication**: Multi-user support with individual progress tracking
- **Advanced Analytics**: Detailed performance metrics and learning curves
- **Topic Categories**: Organize subjects by Physics, Chemistry, Biology
- **Study Streaks**: Gamification elements with achievement badges
- **Export/Import**: Backup and restore functionality
- **Mobile App**: Native mobile applications for iOS and Android
- **Integration**: Connect with calendar applications and notification systems

### Technical Improvements
- **Database Migration**: PostgreSQL for production scalability
- **Caching Layer**: Redis for improved performance
- **API Documentation**: OpenAPI/Swagger documentation
- **Testing Suite**: Unit and integration tests
- **CI/CD Pipeline**: Automated testing and deployment
- **Containerization**: Docker support for easy deployment

## 🤝 Contributing

This project is designed as a portfolio-ready application demonstrating:
- Clean architecture and separation of concerns
- Modern web development practices
- Database design and ORM usage
- Responsive frontend development
- Algorithm implementation for educational purposes

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For any questions or issues regarding the application, please refer to the code documentation or create an issue in the project repository.

---

**Happy Learning! 🎓**

Master your NEET preparation with intelligent, adaptive spaced repetition.
