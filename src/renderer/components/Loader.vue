<template>
    <div>
      <div id="waves"></div>
      <div class="home-container">
        <div class="loader" aria-label="Loading..."></div>
        <div class="random-quotes" v-for="(fact, index) in visibleQuotes" :key="index">
          {{ fact }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  const start = () => {
    router.push('/hello');
  };
  
  const wellnessQuotes = [
    "Live in the now.",
    "Breathe deeply; it's your anchor to the present.",
    "Your body is your temple—treat it with care.",
    "Happiness blooms where mindfulness is planted.",
    "Small steps lead to big transformations.",
    "You are enough just as you are.",
    "Embrace progress, not perfection.",
    "Self-care is not a luxury; it’s a necessity.",
    "Let go of what no longer serves you.",
    "Find joy in the little things.",
    "Balance is the key to a fulfilled life.",
    "Gratitude turns what you have into enough.",
    "Your energy is your currency—spend it wisely.",
    "Rest is just as important as action.",
    "Nourish your soul with what makes you happy.",
    "Strength grows in moments when you think you can’t go on but do anyway.",
    "Peace begins within.",
    "A healthy mind creates a healthy life.",
    "Be kind to yourself—it sets the tone for how others treat you.",
    "Let your light shine; the world needs your glow.",
    "Every sunrise is an opportunity to reset.",
    "Your mind is a garden; tend it with positivity.",
    "Inhale courage, exhale fear.",
    "Simplify your life to amplify your happiness.",
    "Your journey is unique—walk it with pride.",
    "Feel the earth beneath your feet; it grounds you.",
    "Listen to your body—it speaks the truth.",
    "What you think, you become. Choose your thoughts wisely.",
    "True wellness is harmony between body, mind, and soul.",
    "You deserve the love you give to others.",
    "Health is the real wealth.",
    "Let your heart guide you to what feels right.",
    "Drink water like it's a gift.",
    "Rest is productive.",
    "Kindness starts with being kind to yourself.",
    "Every breath is a fresh start.",
    "Don’t rush; the good things take time.",
    "Celebrate small victories—they're steps to big dreams.",
    "You don’t have to do it all to have it all.",
    "Nature heals the soul—spend time in it.",
    "Release what you cannot control.",
    "Your smile is your greatest accessory.",
    "Healing is not linear, and that's okay.",
    "Create space for things that bring you peace.",
    "You're stronger than you think.",
    "Feed your body, mind, and spirit well.",
    "Pause when life feels overwhelming.",
    "Learn to say no without guilt.",
    "Choose connection over comparison.",
    "Beauty is a reflection of inner peace.",
    "Stillness is where clarity begins.",
    "Be gentle with your growth.",
    "The most important relationship is with yourself.",
    "Joy comes from appreciating the present.",
    "Laughter is medicine for the soul.",
    "Honor your boundaries—they protect your peace.",
    "Trust the process of your healing journey.",
    "It’s okay to rest before you feel burnt out.",
    "Let go of judgment—it only weighs you down.",
    "You don’t need to be perfect to inspire others.",
    "Seek calm, not chaos.",
    "Surround yourself with positive energy.",
    "Wellness begins with self-awareness.",
    "Time spent on self-care is never wasted.",
    "Your breath is the bridge between body and mind.",
    "Happiness is found in the present moment.",
    "Your worth is not measured by your productivity.",
    "Reconnect with what makes you feel alive.",
    "Change is uncomfortable, but it’s how we grow.",
    "Self-love is the foundation of all love.",
    "Focus on what you can control and release the rest.",
    "Life flows more easily when you let it.",
    "You’re not alone in this journey.",
    "Every day is a second chance to thrive.",
    "Celebrate progress, not perfection.",
    "Treat yourself as you would a dear friend.",
    "Let the sunshine warm your spirit.",
    "Boundaries are a sign of self-respect.",
    "Turn your pain into power.",
    "Find the rhythm that feels right for you.",
    "A quiet mind is a happy mind.",
    "Stay grounded; you are unshakable.",
    "Your path is uniquely yours.",
    "Let your breath guide you through challenges.",
    "Kind words to yourself fuel resilience.",
    "Growth is messy, but it’s beautiful.",
    "Be patient with your healing.",
    "Let gratitude shape your attitude.",
    "Drink in the beauty of the present moment.",
    "Self-care is how you reclaim your power.",
    "Every step forward is worth celebrating.",
    "Listen to the whispers of your heart.",
    "Calm is contagious—spread it widely.",
    "Love yourself fiercely and without apology.",
    "A peaceful mind leads to a peaceful life.",
    "Plant seeds of positivity daily.",
    "Life isn’t a race; take your time.",
    "Self-compassion is the best gift you can give yourself.",
    "Let go of the rush and embrace the flow.",
    "Choose kindness, especially toward yourself."
  ];
  
  // Reactive array for currently visible quotes
  const visibleQuotes = ref<string[]>([]);
  
  // Function to add and remove quotes
  const manageQuotes = () => {
    // Display the first quote immediately
    if (wellnessQuotes.length && visibleQuotes.value.length < 3) {
      const randomIndex = Math.floor(Math.random() * wellnessQuotes.length);
      const quote = wellnessQuotes[randomIndex];
      visibleQuotes.value.push(quote);
  
      // Remove the first quote after 6 seconds
      setTimeout(() => {
        visibleQuotes.value.shift();
      }, 6000); // Visible for 6 seconds
    }
  
    // Set up an interval for subsequent quotes every 6 seconds
    setInterval(() => {
      if (wellnessQuotes.length && visibleQuotes.value.length < 3) {
        const randomIndex = Math.floor(Math.random() * wellnessQuotes.length);
        const quote = wellnessQuotes[randomIndex];
        visibleQuotes.value.push(quote);
  
        // Remove the quote after 6 seconds
        setTimeout(() => {
          visibleQuotes.value.shift();
        }, 6000); // Visible for 6 seconds
      }
    }, 6000); // Add a new quote every 6 seconds
  };
  
  // Automatically start navigation after 20 seconds
  onMounted(() => {
    manageQuotes(); // Start showing quotes
    setTimeout(() => {
      start();
    }, 5000); // Wait for 20 seconds before navigating
  });
  </script>
  
  <style scoped>
  /* Styling for the loader */
  .loader {
    --r1: 154%;
    --r2: 68.5%;
    width: 60px;
    aspect-ratio: 1;
    border-radius: 50%;
    background:
      radial-gradient(var(--r1) var(--r2) at top, #0000 79.5%, #046997 80%),
      radial-gradient(var(--r1) var(--r2) at bottom, #046997 79.5%, #0000 80%),
      radial-gradient(var(--r1) var(--r2) at top, #0000 79.5%, #046997 80%),
      #ccc;
    background-size: 50.5% 220%;
    background-position: -100% 0%, 0% 0%, 100% 0%;
    background-repeat: no-repeat;
    animation: l9 5s infinite linear;
  }
  
  @keyframes l9 {
    33% {
      background-position: 0% 33%, 100% 33%, 200% 33%;
    }
    66% {
      background-position: -100% 66%, 0% 66%, 100% 66%;
    }
    100% {
      background-position: 0% 100%, 100% 100%, 200% 100%;
    }
  }
  
  .home-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #FFFAF1;
    position: relative;
  }
  
  .random-quotes {
    position: absolute;
    bottom: 10%;
    font-size: 1.2rem;
    background: rgba(255, 255, 255, 0.8);
    padding: 10px 20px;
    border-radius: 8px;
  }
  
  @keyframes fadeInOut {
    0% {
      opacity: 0;
      transform: translateY(20px);
    }
    10% {
      opacity: 1;
      transform: translateY(0);
    }
    90% {
      opacity: 1;
      transform: translateY(0);
    }
    100% {
      opacity: 0;
      transform: translateY(-20px);
    }
  }
</style>  