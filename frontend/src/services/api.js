import axios from 'axios';

const api = axios.create({
  timeout: 300000, // 5 minutes (generation can be slow)
});

export const ENDPOINTS = {
  generateFromDescription: "https://hasratmd697--music-generator-musicgenserver-generate-fro-6c1849.modal.run",
  generateWithLyrics: "https://hasratmd697--music-generator-musicgenserver-generate-wit-ba449d.modal.run",
  generateWithDescribedLyrics: "https://hasratmd697--music-generator-musicgenserver-generate-wit-a2ff74.modal.run",
};

export default api;
