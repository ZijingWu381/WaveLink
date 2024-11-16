<template>
      <div>
        <div id="waves"></div>
        <div class="home-container">
          <h1 class="stylized-text">Welcome to WaveLink</h1>
          <button style="z-index: 10;" @click="start">Start</button>
        </div>
      </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import waves from 'nice-waves'
  
  const router = useRouter()
  
  const start = () => {
    router.push('/hello')
  }
  
  onMounted(() => {
    waves({
      fills: ['rgba(23, 31, 64, 0.5)', 'rgba(130, 192, 175, 0.5)'],
      flowRate: 2,
      swayRate: 0.9,
      wavelength: 10,
      offset: 0.12
    }).mount()
  })
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');
  
  body {
    margin: 0; /* Remove margins from the body */
  }
  
  .home-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: #f5f5f5;
  }
  
  .stylized-text {
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 3rem;
    background: linear-gradient(90deg, #2196F3, #21CBF3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #1976D2;
  }
  
  #waves {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 200px;
  }
  </style>