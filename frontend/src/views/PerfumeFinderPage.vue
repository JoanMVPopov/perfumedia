<template>
  <div class="min-h-screen bg-[#FFF4EA] flex">
    <!-- ========== LEFT STICKY TABLE OF CONTENTS ========== -->
    <aside class="sticky top-20 w-1/6 h-screen border-r p-4 bg-[#FFF4EA] flex-shrink-0">
      <h2 class="text-xl font-bold mb-4">Table of Contents</h2>
      <nav class="flex flex-col space-y-2">
        <!-- Clickable anchor links to each section -->
        <a href="#build-your-own" class="text-black-500 hover:underline">
          I. Build Your Own
        </a>
        <a href="#second-section" class="text-black-500 hover:underline">
          II. Second Section
        </a>
      </nav>
    </aside>

    <!-- ========== MAIN CONTENT AREA ========== -->
    <div class="flex-1 p-6">
      <!-- ~~~~~ SECTION I: BUILD YOUR OWN ~~~~~ -->
      <section id="build-your-own" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">I. Build Your Own Perfume</h1>

        <!-- ===== SUBSECTION 1.1: Perfume Notes ===== -->
        <!-- Updated Perfume Notes section -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4">Select Perfume Notes</h2>
          <div class="flex flex-row space-x-4">
            <!-- Dropdown for selecting notes -->
            <div class="w-64">
              <v-select
                :options="availableNotes"
                v-model="selectedNote"
                placeholder="Select a perfume note"
                label="name"
              ></v-select>
            </div>

            <!-- Selected notes display area -->
            <div class="flex flex-wrap gap-2 p-2 bg-white/50 rounded-lg">
              <div
                v-if="selectedNotes.length === 0"
                class="flex items-center bg-white px-3 py-1 rounded-lg shadow-sm hover:shadow transition-shadow"
              > No notes selected </div>
              <div
                v-else
                v-for="(note, index) in selectedNotes"
                :key="index"
                class="flex items-center bg-white px-3 py-1 rounded-lg shadow-sm hover:shadow transition-shadow"
              >
                <span
                    class="mr-2">{{ note }}
                </span>
                <button
                  @click="removeNote(index)"
                  class="text-gray-500 hover:text-red-500 focus:outline-none"
                  aria-label="Remove note"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== SUBSECTION 1.2: Pie Charts ===== -->
        <!-- Updated Pie Charts section -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold mb-4">Customize Pie Charts</h2>

        <div
          v-for="(pie, pieIndex) in pieCharts"
          :key="pieIndex"
          class="mb-8 border p-4 rounded"
        >
          <h3 class="text-lg font-bold mb-2">
            Pie Chart for {{categories[pieIndex]}}
          </h3>

          <!-- Total percentage warning -->
          <div
            :class="getTotalPercentage(pieIndex) !== 100
            ? 'text-[#C96868] mb-2'
            : 'text-[#7EACB5] mb-2'"
          >
            Total must equal 100% (Current: {{getTotalPercentage(pieIndex)}}%)
          </div>

          <!-- Pie Chart segments -->
          <div
            v-for="(segment, segIndex) in pie.segments"
            :key="segIndex"
            class="flex items-center space-x-4 mb-4"
          >
            <!-- Dropdown for selecting an item -->
            <v-select
              :options="formattedPieItems(pieIndex)"
              v-model="segment.selectedItem"
              placeholder="Select item"
              label="name"
              class="w-48"
              @input="updateChart(pieIndex)"
            ></v-select>

            <!-- Slider for segment percentage -->
            <div class="flex-1 flex items-center space-x-2">
              <input
                type="range"
                v-model.number="segment.percentage"
                min="0"
                max="100"
                class="w-full"
                @input="handleSliderInput(pieIndex, segIndex)"
                @change="finalizeSliderChange(pieIndex)"
              />
              <span class="w-12 text-right">{{segment.percentage}}%</span>
            </div>

            <!-- Button to remove the segment -->
            <button
              @click="removeSegment(pieIndex, segIndex)"
              class="bg-red-500 text-white px-2 py-1 rounded"
              :disabled="pie.segments.length <= 1"
            >
              Remove
            </button>
          </div>

          <!-- Button to add a new segment -->
          <button
            @click="addSegment(pieIndex)"
            class="bg-green-500 text-white px-3 py-1 rounded mb-4"
            :disabled="getTotalPercentage(pieIndex) >= 100"
          >
            Add Segment
          </button>

          <!-- Canvas for Chart.js pie chart -->
          <div class="w-full" style="height:300px;">
            <canvas :id="'pieChart' + pieIndex"></canvas>
          </div>
        </div>
      </div>
      </section>

      <!-- ~~~~~ SECTION II: PLACEHOLDER FOR FUTURE CONTENT ~~~~~ -->
      <section id="second-section" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">II. Second Section (Coming Soon)</h1>
        <p class="text-gray-600">
          This section will be implemented in future updates.
        </p>
      </section>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

// Import Chart.js and register the necessary elements
import {
  Chart,
  PieController,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
Chart.register(PieController, ArcElement, Tooltip, Legend);

export default {
  name: "BuildYourOwnPage",
  components: {
    vSelect,
  },
  data() {
    return {
      // Data for perfume notes (Subsection 1.1)
      sliderTimeout: null,
      perfumeNotes: [],
      selectedNotes: [],
      selectedNote: null,
      // Data for items to be used in pie charts (Subsection 1.2)
      // pieItems: [[], [], [], []],
      pieItems: [],
      categories: ['type', 'style', 'season', 'occasion'],

      // Array of 4 pie charts. Each chart has an array of segments.
      // Each segment contains a selected item and a percentage value.
      pieCharts: [
        { segments: [{ selectedItem: null, percentage: 0 }] },
        { segments: [{ selectedItem: null, percentage: 0 }] },
        { segments: [{ selectedItem: null, percentage: 0 }] },
        { segments: [{ selectedItem: null, percentage: 0 }] },
      ],

      // Array to store Chart.js instances (one for each pie chart)
      chartInstances: [null, null, null, null],
    };
  },
  computed: {
    // Filter out already selected notes from the dropdown options
    availableNotes() {
      return this.perfumeNotes.filter(
        note => !this.selectedNotes.some(selected => selected === note)
      );
    },
  },
  mounted() {
    this.fetchPerfumeNotes();
    this.fetchPieItems();

    // Initialize charts for each pie chart (with initial segments)
    this.pieCharts.forEach((_, index) => {
      this.updateChart(index);
    });
  },
  watch: {
    selectedNote() {
      this.handleNoteSelection()
    }
  },
  methods: {
    formattedPieItems(index) {
    // Ensure the array exists before trying to filter it.
    const items = this.pieItems[index] || [];
    return items
      .filter(item =>
        !this.pieCharts[index].segments.some(
          segment => segment.selectedItem && segment.selectedItem.value === item
        )
      )
      .map(item => ({ name: item, value: item }));
  },
    // Updated note selection handler
    handleNoteSelection() {
      if (this.selectedNote !== null) {
        this.selectedNotes.push(this.selectedNote);
        console.log(this.selectedNotes)
        console.log(this.selectedNote)
        this.selectedNote = null;
      }
    },
    // Updated note removal handler
    removeNote(index) {
      this.selectedNotes.splice(index, 1);
    },
    // Fetch perfume notes from the backend
    fetchPerfumeNotes() {
      apiClient
        .get("/test/pf-perfume-notes")
        .then((response) => {
          console.log(response.data.notes);
          this.perfumeNotes = response.data.notes;
        })
        .catch((error) => {
          console.error("Error fetching perfume notes:", error);
        });
    },
    // Fetch pie chart items from the backend
    fetchPieItems() {
      apiClient
        .get("/test/pf-pie-items")
        .then((response) => {
          console.log(response.data.piechart_items);
          let items;
          items = response.data.piechart_items;
          console.log(items)
          // this.pieItems[0] = items[0];
          // this.pieItems[1] = items[1];
          // this.pieItems[2] = items[2];
          // this.pieItems[3] = items[3];
          this.pieItems.push(items[0]);
          this.pieItems.push(items[1]);
          this.pieItems.push(items[2]);
          this.pieItems.push(items[3]);
          console.log(this.pieItems[0]);
        })
        .catch((error) => {
          console.error("Error fetching pie items:", error);
        });
    },
    // Calculate total percentage for a pie chart
    getTotalPercentage(pieIndex) {
      return this.pieCharts[pieIndex].segments.reduce(
        (sum, segment) => sum + (segment.percentage || 0),
        0
      );
    },

    // Handle slider input with debounce
    handleSliderInput(pieIndex, segIndex) {
      // Clear any existing timeout
      if (this.sliderTimeout) {
        clearTimeout(this.sliderTimeout);
      }

      // Store the current value
      const currentValue = this.pieCharts[pieIndex].segments[segIndex].percentage;

      // Calculate the maximum allowed value for this segment
      const otherSegmentsTotal = this.getTotalPercentage(pieIndex) - currentValue;
      const maxAllowed = 100 - otherSegmentsTotal;

      // Enforce the maximum
      if (currentValue > maxAllowed) {
        this.pieCharts[pieIndex].segments[segIndex].percentage = maxAllowed;
      }
    },

    // Update chart after slider movement ends
    finalizeSliderChange(pieIndex) {
      if (this.sliderTimeout) {
        clearTimeout(this.sliderTimeout);
      }

      this.sliderTimeout = setTimeout(() => {
        this.updateChart(pieIndex);
      }, 100);
    },

    // Modified addSegment method
    addSegment(pieIndex) {
      const currentTotal = this.getTotalPercentage(pieIndex);
      if (currentTotal < 100) {
        this.pieCharts[pieIndex].segments.push({
          selectedItem: null,
          percentage: 0,
        });
        this.$nextTick(() => {
          this.updateChart(pieIndex);
        });
      }
    },

    // Modified removeSegment method
    removeSegment(pieIndex, segIndex) {
      if (this.pieCharts[pieIndex].segments.length > 1) {
        this.pieCharts[pieIndex].segments.splice(segIndex, 1);
        this.$nextTick(() => {
          this.updateChart(pieIndex);
        });
      }
    },

    // Helper method to choose a color based on an index
    getColor(index) {
      const colors = [
        "#FF6384",
        "#36A2EB",
        "#FFCE56",
        "#4BC0C0",
        "#9966FF",
        "#FF9F40",
      ];
      return colors[index % colors.length];
    },
    // Update (or create) the pie chart for a given pie index
    updateChart(pieIndex) {
      const segments = this.pieCharts[pieIndex].segments;
      const labels = segments.map((seg) =>
        seg.selectedItem ? seg.selectedItem.name : "Segment"
      );
      const data = segments.map((seg) => seg.percentage);

      // If a previous Chart.js instance exists, destroy it
      if (this.chartInstances[pieIndex]) {
        this.chartInstances[pieIndex].destroy();
      }
      // Get the canvas element by its id
      const canvasElement = document.getElementById("pieChart" + pieIndex);
      if (!canvasElement) return;
      const ctx = canvasElement.getContext("2d");

      // Create a new Chart.js pie chart instance
      this.chartInstances[pieIndex] = new Chart(ctx, {
        type: "pie",
        data: {
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: segments.map((_, idx) => this.getColor(idx)),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    },
  },
};
</script>

<style scoped>
/* v-select custom styling */
:deep(.v-select) {
  background-color: white;
  border-radius: 0.375rem;
}

:deep(.v-select .vs__dropdown-toggle) {
  padding: 4px 0;
  border-color: #e2e8f0;
}

:deep(.v-select .vs__selected) {
  margin: 0 2px;
}

:deep(.v-select .vs__search) {
  margin: 0;
}
</style>
