<template>
  <transition name="fade" mode="out-in">
    <router-view />
  </transition>
</template>

<script setup lang="ts">
</script>

<style scoped>
  body {
    margin: 0; /* Remove margins from the body */
  }

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>