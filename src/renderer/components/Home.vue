<template>
  <div>
    <div id="waves"></div>
    <div class="home-container">
      <h1 class="main-text">Welcome to WaveLink.</h1>
      <br>
      <button style="z-index: 10;" @click="start" class="button">Begin Healing</button>
      <br><br><br><br><br><br>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import waves from 'nice-waves'
  
  const router = useRouter()

  const start = () => {
    router.push('/loader')
  }

  onMounted(() => {
    // Initialize the waves effect
    waves({
      fills: ['#3369a3', '#627d9a'],
      flowRate: 2,
      swayRate: 0.9,
      wavelength: 10,
      offset: 0.12
    }).mount()
  })
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

  body {
    margin: 0; /* Remove margins from the body */
  }

  .home-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: #FFFAF1;
  }

  .stylized-text {
    font-family: 'Bebas Neue', sans-serif;
    font-weight: 900;
    font-size: 5rem;
    background: linear-gradient(90deg, #2196F3, #21CBF3, #3369a3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
  }

  .main-text {
    font-family: 'Playfair Display';
    font-weight: 900;
    font-size: 4rem;
    background: #2e3257;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 20px;
  }

  .button {
    background: #2e3257;
    background-size: 300% 100%;
    color: white;
    font-family: 'Playfair Display';
    font-size: 18px;
    font-weight: bold;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }

  #waves {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 200px;
  }
</style>
