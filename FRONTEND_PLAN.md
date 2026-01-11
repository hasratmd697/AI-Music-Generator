# AI Music Generator - Frontend Implementation Plan

## Overview

A modern, visually stunning Vue.js frontend for the AI Music Generator with three distinct music creation modes.

---

## Technology Stack

| Category       | Technology                 | Why                                  |
| -------------- | -------------------------- | ------------------------------------ |
| **Framework**  | Vue.js 3 (Composition API) | Reactive, lightweight, excellent DX  |
| **Build Tool** | Vite                       | Fast HMR, modern bundling            |
| **Styling**    | TailwindCSS + Headless UI  | Rapid styling, accessible components |
| **State**      | Pinia                      | Vue's official state management      |
| **Audio**      | WaveSurfer.js              | Waveform visualization + playback    |
| **Animations** | GSAP or Motion One         | Smooth micro-animations              |
| **Icons**      | Lucide Vue                 | Clean, consistent iconography        |
| **HTTP**       | Axios                      | API calls to Modal endpoints         |

---

## Three Music Generation Modes

### Mode 1: Full Description

**Endpoint:** `generate_from_description`

User provides a complete song description, and AI generates:

- Music prompt (style/genre)
- Lyrics (if not instrumental)
- Audio + Cover art

**UI Elements:**

- Large textarea for song description
- Instrumental toggle
- Duration slider (30s - 180s)
- Generate button

---

### Mode 2: Custom Lyrics

**Endpoint:** `generate_with_lyrics`

User provides exact lyrics + music style prompt.

**UI Elements:**

- Text input for music prompt (genre, BPM, mood)
- Large textarea for lyrics
- Duration/seed/guidance controls
- Generate button

---

### Mode 3: Described Lyrics

**Endpoint:** `generate_with_described_lyrics`

User describes what the lyrics should be about + music style.

**UI Elements:**

- Text input for music prompt
- Textarea for lyrics description
- Advanced settings panel
- Generate button

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  🎵 AI Music Generator                          [Dark Mode] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┬─────────────┬─────────────┐               │
│  │ Description │   Lyrics    │  Described  │  <- Mode Tabs │
│  └─────────────┴─────────────┴─────────────┘               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │              Mode-specific Input Form               │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────┐  ┌───────────────────────────┐   │
│  │   Advanced Settings  │  │      🎵 Generate Music    │   │
│  │   (collapsible)      │  │                           │   │
│  └──────────────────────┘  └───────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                     Results Section                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  [Cover Art]  │  🎵 Now Playing: Generated Track     │   │
│  │               │  ▶️ ━━━━━━━━━━●━━━━━━ 2:45 / 3:00   │   │
│  │               │  [Waveform Visualization]            │   │
│  │               │  Categories: Rave, Funk, Disco       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Generated Lyrics (expandable)                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [⬇️ Download Audio]  [⬇️ Download Cover]  [📋 Share]      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── AppHeader.vue          # Logo, dark mode toggle
│   │   └── AppFooter.vue          # Credits, links
│   │
│   ├── modes/
│   │   ├── ModeSelector.vue       # Tab navigation
│   │   ├── DescriptionMode.vue    # Mode 1 form
│   │   ├── LyricsMode.vue         # Mode 2 form
│   │   └── DescribedLyricsMode.vue # Mode 3 form
│   │
│   ├── controls/
│   │   ├── DurationSlider.vue     # Audio duration control
│   │   ├── SeedInput.vue          # Seed for reproducibility
│   │   ├── GuidanceSlider.vue     # Guidance scale control
│   │   ├── InstrumentalToggle.vue # Toggle for instrumental
│   │   └── AdvancedSettings.vue   # Collapsible settings panel
│   │
│   ├── player/
│   │   ├── AudioPlayer.vue        # Main player with waveform
│   │   ├── WaveformDisplay.vue    # WaveSurfer integration
│   │   └── CoverArtDisplay.vue    # Album cover display
│   │
│   └── results/
│       ├── GenerationResult.vue   # Combined result display
│       ├── LyricsDisplay.vue      # Show generated lyrics
│       ├── CategoryTags.vue       # Genre/category tags
│       └── DownloadButtons.vue    # Download audio/cover
│
├── composables/
│   ├── useGenerateMusic.js        # API call logic
│   ├── useAudioPlayer.js          # Audio playback state
│   └── useNotifications.js        # Toast notifications
│
├── stores/
│   └── musicStore.js              # Pinia store for state
│
├── services/
│   └── api.js                     # Axios instance + endpoints
│
├── assets/
│   └── styles/
│       └── main.css               # Global styles
│
├── App.vue
└── main.js
```

---

## API Integration

```javascript
// services/api.js
const ENDPOINTS = {
  generateFromDescription:
    "https://hasratmd697--music-generator-musicgenserver-generate-fro-6c1849.modal.run",
  generateWithLyrics:
    "https://hasratmd697--music-generator-musicgenserver-generate-wit-ba449d.modal.run",
  generateWithDescribedLyrics:
    "https://hasratmd697--music-generator-musicgenserver-generate-wit-a2ff74.modal.run",
};
```

---

## Key Features

### 1. Loading State

- Skeleton loaders during generation
- Progress indication (generation takes ~60s)
- Cancelable requests

### 2. Audio Player

- WaveSurfer.js waveform visualization
- Play/pause/seek controls
- Volume control
- Playback speed adjustment

### 3. Dark/Light Mode

- System preference detection
- Manual toggle
- Persistent preference (localStorage)

### 4. Responsive Design

- Mobile-first approach
- Works on tablets and desktops
- Touch-friendly controls

### 5. Error Handling

- Toast notifications for errors
- Retry mechanism
- Graceful degradation

---

## Design Aesthetics

| Element        | Style                               |
| -------------- | ----------------------------------- |
| **Colors**     | Deep purple gradients, neon accents |
| **Typography** | Inter or Outfit (Google Fonts)      |
| **Effects**    | Glassmorphism cards, subtle shadows |
| **Animations** | Fade-in, scale-up, waveform pulse   |
| **Buttons**    | Gradient backgrounds, hover glow    |

---

## Implementation Phases

### Phase 1: Foundation (Day 1)

- [ ] Initialize Vite + Vue 3 project
- [ ] Configure TailwindCSS
- [ ] Set up project structure
- [ ] Create basic layout components

### Phase 2: Mode Forms (Day 2)

- [ ] Build ModeSelector with tabs
- [ ] Create all 3 mode forms
- [ ] Add form validation
- [ ] Implement control components (sliders, toggles)

### Phase 3: API Integration (Day 3)

- [ ] Set up Axios with endpoints
- [ ] Create Pinia store
- [ ] Implement generation logic
- [ ] Add loading states

### Phase 4: Results & Player (Day 4)

- [ ] Integrate WaveSurfer.js
- [ ] Build audio player component
- [ ] Display cover art and lyrics
- [ ] Add download functionality

### Phase 5: Polish (Day 5)

- [ ] Add animations and transitions
- [ ] Implement dark mode
- [ ] Responsive testing
- [ ] Error handling and edge cases

---

## Commands to Get Started

```bash
# Create Vue project
cd "d:\Python Scripts\AI Music Generator"
npm create vite@latest frontend -- --template vue

# Install dependencies
cd frontend
npm install
npm install tailwindcss postcss autoprefixer -D
npm install @headlessui/vue @heroicons/vue
npm install pinia axios wavesurfer.js
npm install lucide-vue-next

# Initialize Tailwind
npx tailwindcss init -p

# Run dev server
npm run dev
```

---

## Notes

- Generation takes ~60 seconds - need good loading UX
- Audio is base64 encoded - decode before playing
- Cover image is also base64 - display as data URL
- Consider adding a "history" feature for past generations
