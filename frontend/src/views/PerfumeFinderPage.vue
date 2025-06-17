<script setup>
import 'vue3-carousel/carousel.css'
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'

const carouselConfig = {
  itemsToShow: 1.0,
  wrapAround: false,
  breakpointMode: 'carousel'
}

</script>

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
        <a href="#chat-input" class="text-black-500 hover:underline">
          II. (BETA) Chat Input
        </a>
      </nav>
    </aside>

    <!-- ========== MAIN CONTENT AREA ========== -->
    <div class="flex-1 p-6 w-5/6">
      <!-- ~~~~~ SECTION I: BUILD YOUR OWN ~~~~~ -->
      <section id="build-your-own" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">I. Build Your Own Perfume</h1>
        <p class="text-sm mb-4 text-gray-600">
          Using Parfumo’s data format, build your dream perfume.
          Once you’ve completed all the pie charts, you’ll be able to find perfumes in the <u>current</u> dataset
          that match your description. You can also include specific notes if you already know which ones you like.
        </p>

        <!-- ===== SUBSECTION 1.2: Pie Charts ===== -->
        <!-- Updated Pie Charts section -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4">Customize Pie Charts</h2>

          <Carousel v-bind="carouselConfig" @init="onCarouselInit" @slide-end="onSlideEnd">
              <Slide v-for="(pie, pieIndex) in pieCharts"
                :key="pieIndex">

                <div class="flex-row mb-12">
                  <h3 class="text-lg font-bold mb-2">
                  Pie Chart for {{categories[pieIndex]}}
                  </h3>

                  <!-- Total percentage warning -->
                  <div
                    :class="getTotalPercentage(pieIndex) !== 100
                    ? 'text-red-500 mb-2'
                    : 'text-green-400 mb-2'"
                  >
                    {{getTotalPercentage(pieIndex) !== 100
                      ? `Total must equal 100% (Current: ${getTotalPercentage(pieIndex)}%)`
                      : "Correct percentage allocation"}}
                  </div>

                  <!-- Unassigned segments warning -->
                  <div
                    :class="!currentPieSegmentsAllocated(pieIndex)
                    ? 'text-red-500 mb-2'
                    : 'text-green-400 mb-2'"
                  >
                    {{!currentPieSegmentsAllocated(pieIndex)
                      ? "All segments need to be assigned"
                      : "All segments assigned"}}
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
                      @option:selected="updateChart(pieIndex)"
                    ></v-select>

                    <!-- Slider for segment percentage -->
                    <div class="flex-1 flex items-center space-x-2">
                      <input
                        type="range"
                        v-model.number="segment.percentage"
                        min="1"
                        max="100"
                        class="w-full bg-[#C96868]"
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
                    class="text-white px-3 py-1 rounded mb-4"
                    :class="getTotalPercentage(pieIndex) >= 100 || pieCharts[pieIndex].segments.length >= (pieItems[pieIndex] ? pieItems[pieIndex].length : 0)
                    ? 'bg-green-300 cursor-not-allowed'
                    : 'bg-green-500'"
                    :disabled="getTotalPercentage(pieIndex) >= 100 || pieCharts[pieIndex].segments.length >= (pieItems[pieIndex] ? pieItems[pieIndex].length : 0)"
                  >
                    Add Segment
                  </button>

                  <!-- Canvas for Chart.js pie chart -->
                  <div class="w-full" style="height:300px;">
                    <canvas :id="'pieChart' + pieIndex" :ref="el => chartCanvasRefs[pieIndex] = el"></canvas>
                  </div>
                </div>
              </Slide>

            <template #addons>
              <Navigation />
              <Pagination />
            </template>

          </Carousel>
        </div>

         <!-- ===== SUBSECTION 1.1: Perfume Notes ===== -->
        <!-- Updated Perfume Notes section -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4">(OPTIONAL) Select Perfume Notes</h2>
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

        <div>
          <h2 class="text-xl font-semibold mb-4">Get similar perfumes</h2>

          <div v-if="hasSelectedNotes()">
            <div class="p-4 w-3/6">
              <label class="block mb-2 font-semibold">Adjust Weights</label>

              <div class="flex justify-between text-sm mb-2">
                <span>Weight Pie Charts: {{ (weight_categories*100).toFixed(0) }}%</span>
                <span>Weight Notes: {{ (weight_notes*100).toFixed(0) }}%</span>
              </div>

              <!-- Slider -->
              <input
                type="range"
                min="0" max="1" step="0.01"
                v-model.number="weight_categories"
                class="w-full bg-[#C96868]"
              />
            </div>
          </div>

          <button
          @click="calculateSimilaritiesDefault"
          :disabled="!hasSelectedCategories() || loadingDefaultSimilarities"
          class="text-white px-3 py-1 rounded mb-4"
          :class="{
            'bg-[#C96868] opacity-50 cursor-not-allowed': !hasSelectedCategories() || loadingDefaultSimilarities,
            'bg-[#C96868] opacity-100 cursor-pointer': hasSelectedCategories() && !loadingDefaultSimilarities
          }"
          >
            {{loadingDefaultSimilarities ? "Loading..." : "Calculate similarities"}}
          </button>

          <div v-if="!hasSelectedCategories()" class="mb-4">
            <p class="text-red-400">You need to complete the pie charts before proceeding.</p>
          </div>
        </div>

        <!-- ================== NEW RESULTS SECTION ================== -->
        <!-- Simple grid of cards displaying the image, link, and description -->
        <div v-if="defaultSimilaritiesResult" class="mt-6">
          <div class="relative flex items-center h-12 mb-6">
            <!-- Centered item -->
            <h2 class="mx-auto text-xl font-bold">Results</h2>

            <!-- Right-aligned item -->
            <div class="absolute right-0">
              <p>Sort By:</p>
              <v-select
                :options="['Similarity', 'Scent', 'Longevity', 'Sillage', 'Bottle', 'Value for Money']"
                v-model="selectedDefaultSimilaritySortingOption"
                class="w-48"
                @option:selected="sortSimilaritiesBy(selectedDefaultSimilaritySortingOption, this.defaultSimilaritiesResult.data)"
              ></v-select>
            </div>
          </div>


          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <a
              v-for="(item, index) in defaultSimilaritiesResult.data"
              :key="index"
              :href="item.link"
              target="_blank"
              class="block bg-white shadow rounded p-4"
            >
              <!-- Display the image -->
              <img
                v-if="item.image"
                :src="item.image"
                alt="Perfume"
                class="w-full h-auto mt-2 mb-2 object-cover"
              />

              <!-- Display the description text -->
              <p class="text-gray-500 text-sm">
                {{ item.description }}
              </p>

              <!-- Display the similarity score -->
              <p class="text-gray-700 text-sm mt-2">
                Similarity: {{ (item.similarity*100).toFixed(2) }}%
              </p>
            </a>
          </div>
        </div>


      </section>

      <section id="chat-input" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">II. (BETA) Chat Input</h1>
        <p class="text-sm mb-4 text-gray-600">
          Wouldn’t it be cool to describe the perfume you want in natural language rather than build multiple pie charts? Well, this fine-tuned cross-encoder is just what you need… maybe.
        </p>
        <p class="text-sm mb-4 text-gray-600">
          I used a subset of the collected data to fine-tune the model on triplets consisting of:
          <ul class="list-disc list-inside ml-6">
            <li>a deterministic “anchor” perfume description</li>
            <li>a positively LLM-paraphrased version</li>
            <li>a negatively LLM-paraphrased version</li>
          </ul>
          <br>
          Since this process is manual and not part of the ETL pipeline, the accuracy can be a bit questionable — but I’ll try to update the model periodically. Nevertheless, give it a shot!
        </p>

        <div class="mt-4 flex">
          <input
            v-model="chatInput"
            @keyup.enter="calculateModelSimilarities()"
            :disabled="loadingModelSimilarities"
            type="text"
            placeholder="Type your message..."
            class="flex-grow border p-2 rounded-l-lg focus:outline-none"
          />
          <button
            @click="calculateModelSimilarities()"
            :disabled="loadingModelSimilarities"
            class="bg-[#C96868] text-white p-2 rounded-r-lg hover:bg-blue-600 focus:outline-none"
          >
            Send
          </button>
        </div>

        <div v-if="currentModelSimilarityProgress !== 100 && loadingModelSimilarities">
          <p>Current progress: {{ currentModelSimilarityProgress }}%</p>
          <progress :value="currentModelSimilarityProgress" max="100"></progress>
        </div>

        <!-- ================== MODEL RESULTS SECTION ================== -->
        <div v-if="modelSimilaritiesResult" class="mt-6">
          <div class="relative flex items-center h-12 mb-6">
            <!-- Centered item -->
            <h2 class="mx-auto text-xl font-bold">Results</h2>

            <!-- Right-aligned item -->
            <div class="absolute right-0">
              <p>Sort By:</p>
              <v-select
                :options="['Similarity', 'Scent', 'Longevity', 'Sillage', 'Bottle', 'Value for Money']"
                v-model="selectedDefaultModelSimilaritySortingOption"
                class="w-48"
                @option:selected="sortSimilaritiesBy(selectedDefaultModelSimilaritySortingOption, this.modelSimilaritiesResult)"
              ></v-select>
            </div>
          </div>


          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <a
              v-for="(item, index) in modelSimilaritiesResult"
              :key="index"
              :href="item.link"
              target="_blank"
              class="block bg-white shadow rounded p-4"
            >
              <!-- Display the image -->
              <img
                v-if="item.image"
                :src="item.image"
                alt="Perfume"
                class="w-full h-auto mt-2 mb-2 object-cover"
              />

              <!-- Display the description text -->
              <p class="text-gray-500 text-sm">
                {{ item.description }}
              </p>
            </a>
          </div>
        </div>
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

// TODO:
// Should not be able to submit a segment
// Dropdown is kinda funky

export default {
  name: "BuildYourOwnPage",
  components: {
    vSelect,
  },
  data() {
    return {
      chatInput: "",
      chartCanvasRefs: [],
      loadingDefaultSimilarities: false,
      modelSimilaritiesResult: null,
      loadingModelSimilarities: false,
      currentModelSimilarityProgress: 0,
      // Data for perfume notes (Subsection 1.1)
      sliderTimeout: null,
      perfumeNotes: [],
      selectedNotes: [],
      selectedNote: null,
      selectedDefaultSimilaritySortingOption: "Similarity",
      selectedDefaultModelSimilaritySortingOption: "Similarity",
      // Data for items to be used in pie charts (Subsection 1.2)
      // pieItems: [[], [], [], []],
      pieItems: [],
      categories: ['type', 'style', 'season', 'occasion'],

      // Array of 4 pie charts. Each chart has an array of segments.
      // Each segment contains a selected item and a percentage value.
      pieCharts: [
        { segments: [{ selectedItem: null, percentage: 1 }] },
        { segments: [{ selectedItem: null, percentage: 1 }] },
        { segments: [{ selectedItem: null, percentage: 1 }] },
        { segments: [{ selectedItem: null, percentage: 1 }] },
      ],
      defaultSimilaritiesResult: null,
      // Array to store Chart.js instances (one for each pie chart)
      chartInstances: [null, null, null, null],
      weight_categories: 1.0,
    };
  },
  computed: {
    weight_notes() {
      return 1.0 - this.weight_categories; // Reactively updates when weight1 changes
    },
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
    sortSimilaritiesBy(option, resultObject) {
  switch (option) {
    case "Similarity":
      resultObject.sort((a, b) => b.similarity - a.similarity);
      break;
    case "Scent":
      resultObject.sort((a, b) => b.scent - a.scent);
      break;
    case "Longevity":
      resultObject.sort((a, b) => b.longevity - a.longevity);
      break;
    case "Sillage":
      resultObject.sort((a, b) => b.sillage - a.sillage);
      break;
    case "Bottle":
      resultObject.sort((a, b) => b.bottle - a.bottle);
      break;
    case "Value for Money":
      resultObject.sort((a, b) => b.value_for_money - a.value_for_money);
      break;
  }
},
    hasSelectedNotes(){
      return this.selectedNotes.length >= 1;
    },
    currentPieSegmentsAllocated(index){
      for (let segment of this.pieCharts[index].segments){
        if (segment.selectedItem === null) {
          return false;
        }
      }
      return true;
    },
    hasSelectedCategories(){
      // check if all pie charts sum up to 100
      for (let i=0; i<4; i++){
        if (this.getTotalPercentage(i) < 100) {
          return false;
        }
      }

      for (let segment of this.pieCharts.flatMap(chart => chart.segments)){
        if (segment.selectedItem === null) {
          return false;
        }
      }

      return true;
    },
    onCarouselInit() {
    // When the carousel is initialized, update all charts
    this.pieCharts.forEach((_, index) => {
      this.$nextTick(() => {
        this.updateChart(index);
      });
    });
  },
  onSlideEnd({ currentSlideIndex }) {
  setTimeout(() => {
    this.updateChart(currentSlideIndex);
  }, 100);
},
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
        // console.log(this.selectedNotes)
        // console.log(this.selectedNote)
        this.selectedNote = null;
      }
    },
    // Updated note removal handler
    removeNote(index) {
      this.selectedNotes.splice(index, 1);
    },
    calculateSimilaritiesDefault(){
      this.defaultSimilaritiesResult = null;
      this.loadingDefaultSimilarities = true;

      if (!this.hasSelectedNotes()){
        this.weight_categories = 1.0;
      }

      apiClient
        .post("/test/pf-similarities-default/", {
          w_notes: this.weight_notes,
          w_categories: this.weight_categories,
          notes: this.selectedNotes,
          categories: this.pieCharts.flatMap(chart => chart.segments)
        })
        .then((response) => {
          // console.log(response);
          this.defaultSimilaritiesResult = response;
          this.loadingDefaultSimilarities = false;
        })
        .catch((error) => {
          console.error("Error calculating default similarities:", error);
        });
    },
    async calculateModelSimilarities() {
      this.modelSimilaritiesResult = null;
      this.loadingModelSimilarities = true;
      this.currentModelSimilarityProgress = 0;


      // using this instead of the axios client because there are some problems with streaming responses
      const response = await fetch(process.env.VUE_APP_API_URL + "/test/pf-similarities-model/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query: this.chatInput}),
      });

      // Read the streamed body
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // eslint-disable-next-line no-constant-condition
      while (true) {
        const {value, done} = await reader.read();
        if (done) break;

        const chunkText = decoder.decode(value, {stream: true});
        // chunkText may contain SSE-style lines, e.g. "data: {...}\n\n"
        // // console.log("Chunk received:", chunkText);

        const lines = chunkText.split("\n");
        for (const line of lines) {
          if (line.startsWith("data:")) {
            const jsonPart = line.replace("data:", "").trim();
            if (jsonPart) {
              try {
                const parsed = JSON.parse(jsonPart);
                if (parsed.progress !== undefined) {
                  // console.log(`Progress: ${parsed.progress}%`);
                  this.currentModelSimilarityProgress = parsed.progress;
                }
                if (parsed.final !== undefined) {
                  // console.log("Got final results:", parsed.final);
                  this.modelSimilaritiesResult = parsed.final;
                  this.loadingModelSimilarities = false;
                  await reader.cancel();
                }
              } catch (err) {
                console.error("JSON parse error:", err);
              }
            }
          }
        }
      }

      // console.log("ALL DONE")
    },
    // Fetch perfume notes from the backend
    fetchPerfumeNotes() {
      apiClient
        .get("/test/pf-perfume-notes")
        .then((response) => {
          // console.log(response.data.notes);
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
          let items;
          items = response.data.piechart_items;
          this.pieItems.push(items[0]);
          this.pieItems.push(items[1]);
          this.pieItems.push(items[2]);
          this.pieItems.push(items[3]);
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
      // Get the number of available options for this pie chart.
      const availableOptions = (this.pieItems[pieIndex] || []).length;
      const currentSegmentCount = this.pieCharts[pieIndex].segments.length;

      // If we've reached the maximum number of segments, exit early.
      if (currentSegmentCount >= availableOptions) {
        return;
      }

      // Additionally, ensure the total percentage is less than 100.
      if (this.getTotalPercentage(pieIndex) < 100) {
        this.pieCharts[pieIndex].segments.push({
          selectedItem: null,
          percentage: 1,
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
      setTimeout(() => {
        const canvasElement = this.chartCanvasRefs[pieIndex];
        if (!canvasElement) {
          console.warn(`Canvas for slide ${pieIndex} not found.`);
          return;
        }
        const ctx = canvasElement.getContext("2d");

        if (this.chartInstances[pieIndex]) {
          this.chartInstances[pieIndex].destroy();
        }

        const segments = this.pieCharts[pieIndex].segments;
        const labels = segments.map(seg => (seg.selectedItem ? seg.selectedItem.name : "Segment"));
        const data = segments.map(seg => seg.percentage);

        this.chartInstances[pieIndex] = new Chart(ctx, {
          type: "pie",
          data: {
            labels,
            datasets: [{
              data,
              backgroundColor: segments.map((_, idx) => this.getColor(idx)),
            }],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false, // disable animations
            plugins: {
              tooltip: {
                enabled: true, // disable tooltips if not needed
              },
            },
          },
        });
      }, 50); // Adjust delay as needed
    }
  },
};
</script>

<style scoped>
/* Default vue3-carousel pagination styling */
:deep(.carousel__pagination-button--active) {
  background-color: #C96868 !important;
}
:deep(.carousel__pagination-button) {
  background-color: #FADFA1;
}

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

:deep(.carousel__next) {
  inset-inline-end: 100px;
  background-color: #C96868;
  border-radius: 50%;
  padding: 5px;
  color: white;
}
:deep(.carousel__prev) {
  inset-inline-start: 100px;
  background-color: #C96868;
  border-radius: 50%;
  padding: 5px;
  color: white;
}

</style>
