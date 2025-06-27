# RPG Campaign Assistant - Technical Specification

## Overview
A web-based role-playing game assistant designed to help Dungeon Masters (DMs) prepare campaigns, generate NPCs on-the-fly during sessions, and create session recaps from audio recordings. The tool focuses on collaborative campaign planning with AI assistance.

## Target Systems
- **Primary**: Call of Cthulhu
- **Secondary**: D&D 5e, Pathfinder, and other tabletop RPG systems
- **Design**: System-agnostic architecture to support multiple rule sets

## Core Features

### 1. Collaborative Campaign Planning
- **Interface**: Dynamic, freestyle document editor (similar to collaborative writing apps)
- **Structure**: Flexible organization allowing DMs to use their preferred structure
- **AI Integration**: AI agents assist with:
  - Plot twist suggestions
  - Encounter creation and stat blocks
  - Atmospheric descriptions
  - Session pacing recommendations
  - Location development
  - Story arc refinement
- **Workflow**: Back-and-forth refinement process between DM and AI
- **Final Authority**: DM has final approval on all content

### 2. On-the-Fly NPC Generation
- **Trigger**: Dedicated button/interface within the collaborative document
- **Interface**: Interactive chat interface for parameter specification
- **Parameters**: All potential NPC attributes via conversational input:
  - Role in story (shopkeeper, witness, antagonist, etc.)
  - Personality traits
  - Appearance
  - Relevant skills/stats
  - Relationship to existing campaign elements
- **Agent Focus**: Specialized NPC generation agent (distinct from general campaign assistant)
- **Integration**: Generated NPCs can be added to session notes after DM approval
- **Usage Context**: Available during both session preparation and live gameplay

### 3. Session Recap Generation
- **Input**: Audio recordings uploaded by DM (MP3, WAV formats)
- **Processing**: Speech-to-text transcription with AI-generated summary
- **Content**: Recap includes:
  - What happened during the session
  - Player achievements
  - Gains/rewards obtained
- **Output**: Editable recap document
- **Export**: Sessions downloadable as PDFs

### 4. Discord Integration
- **Authentication**: Support for Discord OAuth
- **Functionality**: Push session recaps to Discord servers
- **Customization**: DM can customize what content gets shared
- **Multi-server**: Support for multiple Discord servers per campaign

## Technical Architecture

### Backend
- **Framework**: Python with FastAPI
- **Database**: Developer's choice (recommend PostgreSQL or MongoDB)
- **Cloud**: No specific preference - developer's discretion
- **AI Integration**: Support for multiple AI models/APIs

### Frontend
- **Type**: Web application (browser-based)
- **Architecture**: Single-user document editing (no real-time collaboration initially)
- **Export**: PDF generation capability

### Authentication
- **Methods**: 
  - Email/password
  - Google OAuth
  - Discord OAuth
- **Account Management**: Standard user registration and management

### File Management
- **Storage**: Cloud-based campaign storage
- **Uploads**: Support for PDF uploads (rulebooks, custom content)
- **Audio**: MP3 and WAV file processing for speech-to-text
- **Export**: PDF download functionality for sessions

## AI Agent Architecture

### Campaign Assistant Agent
- **Scope**: Broad RPG knowledge and campaign planning
- **Capabilities**:
  - Plot development
  - Encounter design
  - Location creation
  - Session planning
  - General RPG assistance

### NPC Generation Agent
- **Scope**: Specialized NPC creation
- **Interface**: Conversational chat interface
- **Parameters**: Dynamic parameter acceptance through natural language
- **Integration**: Seamless addition to campaign documents

### Knowledge Base
- **Official Content**: Access to official rulebooks for supported systems
- **Custom Content**: User-uploaded PDFs and documents
- **System**: Flexible knowledge base supporting multiple RPG systems

## User Experience Flow

### Campaign Creation
1. DM creates new campaign
2. Selects RPG system
3. Uploads relevant rulebooks/PDFs
4. Begins collaborative planning with AI assistant

### Session Preparation
1. DM outlines session goals/plot points
2. AI suggests encounters, locations, NPCs
3. Iterative refinement process
4. Session plan finalization

### Live Session Support
1. Access to campaign documents during play
2. On-demand NPC generation via dedicated interface
3. Real-time document updates

### Post-Session
1. Upload session recording
2. AI generates transcript and recap
3. DM reviews and edits recap
4. Export to PDF and/or push to Discord

## Data Models

### Campaign
- Campaign ID
- Name
- RPG System
- Creation Date
- DM User ID
- Associated Sessions
- Uploaded Documents

### Session
- Session ID
- Campaign ID
- Session Number
- Date
- Preparation Notes
- Generated NPCs
- Audio Recording
- Transcript
- Recap
- Status (Planned/In Progress/Completed)

### NPC
- NPC ID
- Session ID
- Name
- Role
- Attributes
- Generated Parameters
- Integration Status

### User
- User ID
- Email
- Authentication Method
- Subscription Status
- Discord Integration Settings

## Integration Requirements

### Discord API
- Bot creation and management
- Server integration
- Message posting with customizable content
- Multi-server support per user

### Speech-to-Text
- Support for MP3 and WAV formats
- Transcript generation
- Integration with AI summarization

### PDF Generation
- Campaign document export
- Session recap export
- Custom formatting options

## Subscription Model
- **Type**: Subscription-based pricing
- **Tiers**: To be defined based on feature complexity
- **Features**: Differentiated by usage limits, AI capabilities, storage, etc.

## Future Considerations
- Real-time collaboration features
- Mobile application
- Additional RPG system support
- Advanced Discord bot features
- Voice command integration

## Success Metrics
- User engagement with AI suggestions
- NPC generation usage frequency
- Session recap accuracy and usefulness
- Discord integration adoption
- Campaign completion rates

## Development Phases

### Phase 1: Core Platform
- User authentication
- Basic campaign document editor
- AI agent integration framework

### Phase 2: AI Features
- Campaign planning assistant
- NPC generation system
- Knowledge base integration

### Phase 3: Session Management
- Audio upload and transcription
- Recap generation
- PDF export functionality

### Phase 4: Integrations
- Discord integration
- Enhanced export options
- Subscription management

### Phase 5: Polish & Scale
- Performance optimization
- Advanced features
- Multi-system expansion
