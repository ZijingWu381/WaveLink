<template>
  <div :style="{ backgroundColor: colour }" class="dial-container">
    <canvas ref="canvasRef" width="400" height="400" class="dial-canvas"></canvas>
    <div class="dial-info">
      <h3>Synchrony</h3>
      <p>{{ value }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, onUnmounted, computed } from 'vue'
import { io } from 'socket.io-client'

// Canvas and dial parameters
const canvasRef = ref<HTMLCanvasElement | null>(null)
const value = ref(0)
const angle = ref(0)
const colour = ref('grey')
// Declare animationId to store the requestAnimationFrame ID
let animationId: number

// Function to smoothly update the dial angle
const smoothUpdate = (current, target, step = 0.01) => {
  if (Math.abs(current - target) < step) {
    return target
  }
  return current + (target - current) * step
}

// Gradient stops
const gradientStops = [
  { stop: 0, color: '#ff0000' }, // Red
  { stop: 0.15, color: '#ff0000' }, // Red
  { stop: 0.3, color: '#ffff00' }, // Yellow
  { stop: 0.7, color: '#ffff00' }, // Yellow
  { stop: 0.85, color: '#00ff00' }, // Green
  { stop: 1, color: '#00ff00' } // Green
]

// Function to interpolate between two colors
const interpolateColor = (color1, color2, factor) => {
  const hex = (color) => {
    return color.slice(1).match(/.{2}/g).map((hex) => parseInt(hex, 16))
  }

  const [r1, g1, b1] = hex(color1)
  const [r2, g2, b2] = hex(color2)

  const r = Math.round(r1 + (r2 - r1) * factor).toString(16).padStart(2, '0')
  const g = Math.round(g1 + (g2 - g1) * factor).toString(16).padStart(2, '0')
  const b = Math.round(b1 + (b2 - b1) * factor).toString(16).padStart(2, '0')

  return `#${r}${g}${b}`
}

// Function to get the color at a specific point in the gradient
const getColorFromGradient = (ratio) => {
  for (let i = 0; i < gradientStops.length - 1; i++) {
    const start = gradientStops[i]
    const end = gradientStops[i + 1]
    if (ratio >= start.stop && ratio <= end.stop) {
      const factor = (ratio - start.stop) / (end.stop - start.stop)
      return interpolateColor(start.color, end.color, factor)
    }
  }
  return gradientStops[gradientStops.length - 1].color
}
// Computed property to get the background color based on the value
// const backgroundColor = computed(() => {
//   return getColorFromGradient(value.value / 100)
// })

const colourchange = (backval: number) => {
  colour.value = getColorFromGradient(backval / 100)
  console.log(colour.value)
}

// Draw the dial
const drawDial = (ctx: CanvasRenderingContext2D, width: number, height: number, angle: number) => {
  ctx.clearRect(0, 0, width, height)
  
  // Draw the dial background
  ctx.beginPath()
  ctx.arc(width / 2, height / 2, 150, 0.75 * Math.PI, 0.25 * Math.PI, false)
  ctx.fillStyle = '#f5f5f5'
  ctx.fill()
  ctx.strokeStyle = '#ccc'
  ctx.lineWidth = 2
  ctx.stroke()
  
  // Draw tick marks
  for (let i = 0; i <= 100; i += 10) {
    const tickAngle = (i / 100) * 1.5 * Math.PI + 0.75 * Math.PI
    const x1 = width / 2 + 140 * Math.cos(tickAngle)
    const y1 = height / 2 + 140 * Math.sin(tickAngle)
    const x2 = width / 2 + 150 * Math.cos(tickAngle)
    const y2 = height / 2 + 150 * Math.sin(tickAngle)
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.strokeStyle = '#000'
    ctx.lineWidth = 2
    ctx.stroke()
    
    // Draw labels
    const labelX = width / 2 + 120 * Math.cos(tickAngle)
    const labelY = height / 2 + 120 * Math.sin(tickAngle)
    ctx.font = '12px Arial'
    ctx.fillStyle = '#000'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(i.toString(), labelX, labelY)
  }

  // Draw the gauge outline with smoother gradient
  const gradient = ctx.createLinearGradient(0, 0, width, 0)
  gradientStops.forEach(stop => gradient.addColorStop(stop.stop, stop.color))


  ctx.beginPath()
  ctx.arc(width / 2, height / 2, 160, 0.75 * Math.PI, 0.25 * Math.PI, false)
  ctx.strokeStyle = gradient
  ctx.lineWidth = 10
  ctx.stroke()
  
  // Determine the needle color based on the angle
  const backcolour = getColorFromGradient(value.value/100)
  const needleColor = 'black'

  // Draw the dial needle
  ctx.beginPath()
  ctx.moveTo(width / 2, height / 2)
  const x = width / 2 + 140 * Math.cos((angle - 90) * Math.PI / 180)
  const y = height / 2 + 140 * Math.sin((angle - 90) * Math.PI / 180)
  ctx.lineTo(x, y)
  ctx.strokeStyle = needleColor
  ctx.lineWidth = 4
  ctx.stroke()
}

// Animation loop
const animate = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const loop = () => {
    drawDial(ctx, width, height, angle.value)
    animationId = requestAnimationFrame(loop)
  }
  
  requestAnimationFrame(loop)
}

// Function to continuously update the dial angle
const updateDialAngle = (targetValue: number, step: number) => {
  const targetAngle = (targetValue / 100) * 270 - 135 // Map value to angle
  const update = () => {
    angle.value = smoothUpdate(angle.value, targetAngle, step)
    if (angle.value !== targetAngle) {
      requestAnimationFrame(update)
    }
  }
  update()
}

onMounted(() => {
  const socket = io('http://localhost:5000', {
    transports: ['websocket'],
  });

  socket.on('connect', () => {
    console.log('Connected to WebSocket server');
  });

  socket.on('error', (error) => {
    console.error('Socket error:', error);
  });

  socket.on('update_data', (data) => {
    console.log('Received data:', data);
    value.value = data.value
    // Smoothly update the dial angle
    updateDialAngle(data.value, 0.1)

    colourchange(value.value)
  })

  const canvas = canvasRef.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // Start animation
  animate(ctx, canvas.width, canvas.height)
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>
<style scoped>
.dial-container {
  position: relative; /* Ensure the container is positioned relative */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  transition: background-color 0.5s ease; /* Smooth transition for background color */
}

.dial-canvas {
  background: white;
  border: 1px solid #ccc;
  border-radius: 50%; /* Make the canvas circular */
  width: 400px; /* Ensure the width and height are equal */
  height: 400px; /* Ensure the width and height are equal */
}

.dial-info {
  position: absolute; /* Position the dial-info div absolutely */
  top: 50%; /* Position it at the vertical center */
  left: 50%; /* Position it at the horizontal center */
  transform: translate(-50%, 110px); /* Center it horizontally and move it 30px down */
  background: rgba(255, 255, 255, 0.8); /* Optional: Add a background with some transparency */
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  
}
.dial-info h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;
  font-size: 1.5rem;
  background: linear-gradient(90deg, #2196F3, #21CBF3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: -10px;
}

.dial-info p {
  margin: 5px 0;
  color: #666;
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;
  font-size: 1.5rem;
  background: linear-gradient(90deg, #2196F3, #21CBF3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: -10px;
}
</style>