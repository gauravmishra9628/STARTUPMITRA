# VyaparAI - AI Business Builder Platform Specification

## 1. Project Overview

**Project Name:** VyaparAI
**Type:** Full-stack AI-powered startup platform
**Core Functionality:** Help users discover business ideas, create startup plans, get investment estimates, profit analysis, and AI-generated business roadmaps
**Target Users:** Indian entrepreneurs, startup founders, small business owners, students looking for business opportunities

## 2. Tech Stack

### Frontend
- React.js 18+
- Vite (build tool)
- Tailwind CSS
- React Router DOM
- Axios
- Redux Toolkit

### Backend
- Django 4.x
- Django REST Framework
- JWT Authentication
- PostgreSQL (simulated with SQLite for local dev)

### AI Integration
- OpenAI API (GPT-4)
- Gemini API support ready

## 3. UI/UX Specification

### Color Palette
- **Primary:** #0F0F0F (Black)
- **Secondary:** #1E40AF (Blue)
- **Accent:** #7C3AED (Purple)
- **Background:** #0A0A0A (Dark)
- **Card Background:** rgba(30, 30, 30, 0.8) (Glassmorphism)
- **Text Primary:** #FFFFFF
- **Text Secondary:** #A1A1AA
- **Success:** #10B981
- **Warning:** #F59E0B
- **Error:** #EF4444

### Typography
- **Headings:** Inter, system-ui
- **Body:** Inter, sans-serif
- **H1:** 48px, font-weight: 700
- **H2:** 36px, font-weight: 600
- **H3:** 24px, font-weight: 600
- **Body:** 16px, font-weight: 400
- **Small:** 14px, font-weight: 400

### Design Elements
- Glassmorphism cards with backdrop-blur
- Gradient accents (blue to purple)
- Smooth transitions (300ms ease)
- Hover lift effects on cards
- Responsive breakpoints:
  - Mobile: < 640px
  - Tablet: 640px - 1024px
  - Desktop: > 1024px

## 4. Page Structure

### 4.1 Home Page
- Hero section with animated gradient background
- Business categories grid (6 categories)
- AI Mentor showcase cards
- Testimonials carousel
- Pricing section with 3 tiers
- CTA buttons with glow effect
- Footer with links

### 4.2 Authentication Pages
- Login: Email/password form, JWT handling
- Register: Name, email, password, confirm password
- Password visibility toggle
- Form validation with error messages
- Glassmorphism card design

### 4.3 Dashboard
- Welcome banner with user name
- Statistics cards (saved businesses, AI chats, sessions)
- Recent AI chats list
- Quick action buttons
- Sidebar navigation
- Saved business ideas grid

### 4.4 Business Ideas Page
- Search bar with debounce
- Category filter dropdown
- Budget range filter (slider)
- Difficulty filter (Easy/Medium/Hard)
- Business cards grid (9 per page)
- Pagination controls
- Each card shows: title, investment, profit estimate, difficulty badge, description

### 4.5 Business Details Page
- Full business title and category
- Investment analysis section
- Profit estimation with chart
- Risk analysis with indicators
- Marketing strategy accordion
- Required skills tags
- AI-generated roadmap timeline
- Save/Bookmark button
- Share button

### 4.6 AI Mentor Chat Page
- Chat container with messages
- AI avatar and typing indicator
- Message bubbles (user right, AI left)
- Suggested prompt buttons
- Markdown rendering for AI responses
- Chat history sidebar
- Clear chat option

### 4.7 Investment Calculator Page
- Investment amount input
- Monthly expense inputs
- Profit prediction slider
- ROI calculation display
- Simple chart visualization
- AI suggestions panel

### 4.8 Community Page
- Post creation form
- Posts feed with infinite scroll
- Like button with count
- Comment section
- Trending posts sidebar
- User avatars

### 4.9 Admin Dashboard
- Stats overview cards
- User management table
- Business management
- AI usage analytics
- Revenue charts
- Reports section

## 5. Backend Architecture

### Django Apps
1. **accounts** - User authentication, profiles
2. **businesses** - Business ideas CRUD
3. **ai_engine** - AI chat, recommendations
4. **roadmaps** - Business roadmap generation
5. **analytics** - Usage tracking
6. **community** - Posts, comments

### API Endpoints

#### Authentication
- POST /api/auth/register/
- POST /api/auth/login/
- GET /api/auth/profile/
- PUT /api/auth/profile/

#### Businesses
- GET /api/businesses/
- POST /api/businesses/
- GET /api/businesses/{id}/
- PUT /api/businesses/{id}/
- DELETE /api/businesses/{id}/
- GET /api/businesses/search/?q=...

#### AI Engine
- POST /api/ai/chat/
- POST /api/ai/roadmap/
- POST /api/ai/recommend/

#### Community
- GET /api/community/posts/
- POST /api/community/posts/
- POST /api/community/posts/{id}/like/
- POST /api/community/posts/{id}/comments/

## 6. Acceptance Criteria

### Visual Checkpoints
- [ ] Dark theme applied consistently
- [ ] Glassmorphism cards visible on all pages
- [ ] Gradient accents on buttons and highlights
- [ ] Smooth page transitions
- [ ] Mobile responsive on all breakpoints
- [ ] All animations working (hover, typing, etc.)

### Functional Checkpoints
- [ ] User can register and login
- [ ] JWT tokens properly stored and used
- [ ] Business ideas display with filtering
- [ ] AI chat returns responses
- [ ] Calculator computes ROI correctly
- [ ] Community posts can be created and liked
- [ ] Dashboard shows user statistics
- [ ] Admin can manage users and businesses

### Performance
- [ ] Page load < 3 seconds
- [ ] API responses < 500ms
- [ ] Smooth 60fps animations