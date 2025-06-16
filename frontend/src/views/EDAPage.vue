<template>
  <div class="min-h-screen bg-[#FFF4EA] flex">
    <!-- ========== LEFT STICKY TABLE OF CONTENTS ========== -->
    <aside class="sticky top-20 w-1/6 h-screen border-r p-4 bg-[#FFF4EA] flex-shrink-0">
      <h2 class="text-xl font-bold mb-4">Table of Contents</h2>
      <nav class="flex flex-col space-y-2">
        <!-- Clickable anchor links to each section -->
        <a href="#ratings" class="text-black-500 hover:underline">
          I. Ratings
        </a>
        <a href="#ratings-progression" class="text-black-500 hover:underline">
          II. Ratings progression
        </a>
        <a href="#categories-and-notes" class="text-black-500 hover:underline">
          III. Categories &amp; Notes
        </a>
        <a href="#correlation" class="text-black-500 hover:underline">
          IV. Correlation
        </a>
        <a href="#brands" class="text-black-500 hover:underline">
          V. Brands
        </a>
      </nav>
    </aside>

    <!-- ========== MAIN CONTENT AREA ========== -->
    <div class="flex-1 p-6">
      <!-- ~~~~~ SECTION I: RATINGS (ALREADY STYLED) ~~~~~ -->
      <section id="ratings" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">I. Ratings</h1>
        <p class="text-sm mb-4 text-gray-600">
          This section presents “static” snapshots of rating data for one or two filter sets.
          You’ll see descriptive‐statistic tables, box plots, pair‐plots, QQ plots, and violin plots,
          which should help you get a sense of the central tendency, spread, distribution shape, and pairwise relationships among the perfume ratings.
        </p>

        <!-- ========== FILTERS FOR RATINGS ========== -->
        <div class="mb-6 flex flex-col">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>

          <!-- First row: Set 1, Compare With button, and Set 2 -->
          <div class="flex"
          :class="!showSecondOptions.ratings
          ? 'items-center space-x-6'
          : 'items-center justify-center gap-x-20'">
            <!-- Set 1 -->
            <div class="flex space-x-4">
              <!-- Decade (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="ratingsDecade1" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.ratings.set1.decade"
                  id="ratingsDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <!-- Gender (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="ratingsGender1" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.ratings.set1.gender"
                  id="ratingsGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>

            <!-- Compare With button -->
            <div>
              <button
                v-if="!showSecondOptions.ratings"
                @click="toggleSecondOptions('ratings')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Compare with...
              </button>

              <button
                v-else
                @click="toggleSecondOptions('ratings')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Remove comparison
              </button>
            </div>

            <!-- Set 2 (shown if toggled) -->
            <div v-if="showSecondOptions.ratings" class="flex space-x-4">
              <!-- Decade (Set 2) -->
              <div class="flex flex-col w-32">
                <label for="ratingsDecade2" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.ratings.set2.decade"
                  id="ratingsDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <!-- Gender (Set 2) -->
              <div class="flex flex-col w-32">
                <label for="ratingsGender2" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.ratings.set2.gender"
                  id="ratingsGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>
          </div>

          <div class="mt-4"
          :class="!showSecondOptions.ratings
          ? 'self-start'
          : 'self-center'">
            <button
              @click="fetchRatings"
              :disabled="loading1"
              class="bg-[#C96868] text-white py-2 px-4 rounded-md
                     hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]"
            >
              {{loading1 ? "Loading..." : "Get Ratings"}}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="error1" class="mt-4 text-red-600 font-medium text-center">
          {{ error1 }}
        </p>

        <!-- ========== DISPLAY RATINGS IMAGES ========== -->
        <div
          :class="showTwoColumns('ratings')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- ====== SET 1 IMAGES ====== -->
          <div
            v-if="images.ratings[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div
              v-if="!showTwoColumns('ratings')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.ratings[0]"
                  :key="'rat1-' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div ref="imageViewer" class="flex-shrink-0 max-w-[70%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation w/ typewriter text -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices1.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index, expandedIndices1, displayedText, textToDisplay, typingIntervals1)"
                    >
                      {{ expandedIndices1.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices1.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          {{displayedText[index % textToDisplay.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images in a scroll container -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.ratings[0]"
                  :key="'rat1-col2-' + index"
                  class="border-b pb-4 mb-4"
                >
                  <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- ====== SET 2 IMAGES ====== -->
          <div
            v-if="showSecondOptions.ratings && images.ratings[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div class="overflow-y-auto h-full">
              <ul>
                <li
                  v-for="(image, index) in images.ratings[1]"
                  :key="'rat2-' + index"
                  class="border-b pb-4 mb-4"
                >
                  <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>


      <!-- ~~~~~ SECTION II: RATINGS PROGRESSION (UPDATED STYLING) ~~~~~ -->
      <section id="ratings-progression" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">II. Ratings progression</h1>
        <p class="text-sm mb-4 text-gray-600">
          Shows how average ratings evolve over time for the selected decade/gender filters.
          Line charts plot yearly means with shaded regions (± 1 SD), revealing trends, fluctuations, and the consistency of reviews across years.
        </p>

        <!-- ========== FILTERS (Progression) ========== -->
        <div class="mb-6 flex flex-col">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>

          <!-- First row: Set 1, Compare With button, and Set 2 -->
          <div
            class="flex"
            :class="!showSecondOptions.ratingsProgression
              ? 'items-center space-x-6'
              : 'items-center justify-center gap-x-20'"
          >
            <!-- Set 1 -->
            <div class="flex space-x-4">
              <!-- Decade (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="progressionDecade1" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.ratingsProgression.set1.decade"
                  id="progressionDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                </select>
              </div>
              <!-- Gender (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="progressionGender1" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.ratingsProgression.set1.gender"
                  id="progressionGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>

            <!-- Compare With button -->
            <div>
              <button
                v-if="!showSecondOptions.ratingsProgression"
                @click="toggleSecondOptions('ratingsProgression')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Compare with...
              </button>

              <button
                v-else
                @click="toggleSecondOptions('ratingsProgression')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Remove comparison
              </button>
            </div>

            <!-- Set 2 (shown if toggled) -->
            <div
              v-if="showSecondOptions.ratingsProgression"
              class="flex space-x-4"
            >
              <div class="flex flex-col w-32">
                <label for="progressionDecade2" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.ratingsProgression.set2.decade"
                  id="progressionDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="progressionGender2" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.ratingsProgression.set2.gender"
                  id="progressionGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Fetch button aligned similarly -->
          <div
            class="mt-4"
            :class="!showSecondOptions.ratingsProgression
              ? 'self-start'
              : 'self-center'"
          >
            <button
              @click="fetchRatingsProgression"
              :disabled="loading2"
              class="bg-[#C96868] text-white py-2 px-4 rounded-md
                     hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]"
            >
              {{loading2 ? "Loading..." : "Get Ratings progression"}}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="error2" class="mt-4 text-red-600 font-medium text-center">
          {{ error2 }}
        </p>

        <!-- DISPLAY RATINGS PROGRESSION IMAGES -->
        <div
          :class="showTwoColumns('ratingsProgression')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
            v-if="images.ratingsProgression[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div
              v-if="!showTwoColumns('ratingsProgression')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.ratingsProgression[0]"
                  :key="'rat1-prog1' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div ref="imageViewer" class="flex-shrink-0 max-w-[70%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation w/ typewriter text -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices2.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index, expandedIndices2, displayedText2, textToDisplay2, typingIntervals2)"
                    >
                      {{ expandedIndices2.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices2.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          {{ displayedText2[index % textToDisplay2.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images in a scroll container -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.ratingsProgression[0]"
                  :key="'rat1-col2-' + index"
                  class="border-b pb-4 mb-4"
                >
                  <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Set 2 -->
          <div
            v-if="showSecondOptions.ratingsProgression && images.ratingsProgression[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <ul>
              <li
                v-for="(image, idx) in images.ratingsProgression[1]"
                :key="'prog2-' + idx"
                class="border-b pb-4 mb-4"
              >
                <div ref="imageViewer">
                  <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Progression Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                  />
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>


      <!-- ~~~~~ SECTION III: Categories & Notes (UPDATED STYLING) ~~~~~ -->
      <section id="categories-and-notes" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">III. Categories &amp; Notes</h1>
        <p class="text-sm mb-4 text-gray-600">
          Visualizes fragrance categories and the prevalence of individual scent notes.
          You’ll get pie charts of category proportions and a bar chart of the top notes by frequency,
          highlighting which styles and ingredients dominate.
        </p>

        <!-- FILTERS -->
        <div class="mb-6 flex flex-col">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>

          <!-- First row: Set 1, Compare With button, and Set 2 -->
          <div
            class="flex"
            :class="!showSecondOptions.categoriesAndNotes
              ? 'items-center space-x-6'
              : 'items-center justify-center gap-x-20'"
          >
            <!-- Set 1 -->
            <div class="flex space-x-4">
              <!-- Decade (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="catDecade1" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.categoriesAndNotes.set1.decade"
                  id="catDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <!-- Gender (Set 1) -->
              <div class="flex flex-col w-32">
                <label for="catGender1" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.categoriesAndNotes.set1.gender"
                  id="catGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>

            <!-- Compare With button -->
            <div>
              <button
                v-if="!showSecondOptions.categoriesAndNotes"
                @click="toggleSecondOptions('categoriesAndNotes')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Compare with...
              </button>

              <button
                v-else
                @click="toggleSecondOptions('categoriesAndNotes')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Remove comparison
              </button>
            </div>

            <!-- Set 2 -->
            <div
              v-if="showSecondOptions.categoriesAndNotes"
              class="flex space-x-4"
            >
              <div class="flex flex-col w-32">
                <label for="catDecade2" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.categoriesAndNotes.set2.decade"
                  id="catDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="catGender2" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.categoriesAndNotes.set2.gender"
                  id="catGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Action button, styled the same -->
          <div
            class="mt-4"
            :class="!showSecondOptions.categoriesAndNotes
              ? 'self-start'
              : 'self-center'"
          >
            <button
              @click="fetchCategoriesAndNotes"
              :disabled="loading3"
              class="bg-[#C96868] text-white py-2 px-4 rounded-md
                     hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]"
            >
              {{loading3 ? "Loading..." : "Get Categories & Notes"}}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="error3" class="mt-4 text-red-600 font-medium text-center">
          {{ error3 }}
        </p>

        <!-- DISPLAY IMAGES -->
        <div
          :class="showTwoColumns('categoriesAndNotes')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
            v-if="images.categoriesAndNotes[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div
              v-if="!showTwoColumns('categoriesAndNotes')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.categoriesAndNotes[0]"
                  :key="'rat1-prog1' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div ref="imageViewer" class="flex-shrink-0 max-w-[70%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation w/ typewriter text -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices3.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index, expandedIndices3, displayedText3, textToDisplay3, typingIntervals3)"
                    >
                      {{ expandedIndices3.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices3.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          {{ displayedText3[index % textToDisplay3.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.categoriesAndNotes[0]"
                  :key="'rat1-col2-' + index"
                  class="border-b pb-4 mb-4"
                >
                  <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Set 2 -->
          <div
            v-if="showSecondOptions.categoriesAndNotes && images.categoriesAndNotes[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <ul>
              <li
                v-for="(image, idx) in images.categoriesAndNotes[1]"
                :key="'cat2-' + idx"
                class="border-b pb-4 mb-4"
              >
                <div ref="imageViewer">
                  <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Decoded Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                  />
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>


      <!-- ~~~~~ SECTION IV: Correlation (UPDATED STYLING) ~~~~~ -->
      <section id="correlation" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">IV. Correlation</h1>
        <p class="text-sm mb-4 text-gray-600">
          Uses heatmaps to explore relationships between metadata and ratings
        </p>

        <!-- FILTERS -->
        <div class="mb-6 flex flex-col">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>

          <!-- First row: Set 1, Compare With, and Set 2 -->
          <div
            class="flex"
            :class="!showSecondOptions.correlation
              ? 'items-center space-x-6'
              : 'items-center justify-center gap-x-20'"
          >
            <!-- Set 1 -->
            <div class="flex space-x-4">
              <div class="flex flex-col w-32">
                <label for="corrDecade1" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.correlation.set1.decade"
                  id="corrDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="corrGender1" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.correlation.set1.gender"
                  id="corrGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>

            <!-- Compare With button -->
            <div>
              <button
                v-if="!showSecondOptions.correlation"
                @click="toggleSecondOptions('correlation')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Compare with...
              </button>

              <button
                v-else
                @click="toggleSecondOptions('correlation')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Remove comparison
              </button>
            </div>

            <!-- Set 2 -->
            <div
              v-if="showSecondOptions.correlation"
              class="flex space-x-4"
            >
              <div class="flex flex-col w-32">
                <label for="corrDecade2" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.correlation.set2.decade"
                  id="corrDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="corrGender2" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.correlation.set2.gender"
                  id="corrGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Action button -->
          <div
            class="mt-4"
            :class="!showSecondOptions.correlation
              ? 'self-start'
              : 'self-center'"
          >
            <button
              @click="fetchCorrelation"
              :disabled="loading4"
              class="bg-[#C96868] text-white py-2 px-4 rounded-md
                     hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]"
            >
              {{loading4 ? "Loading..." : "Get Correlation"}}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="error4" class="mt-4 text-red-600 font-medium text-center">
          {{ error4 }}
        </p>

        <!-- DISPLAY IMAGES -->
        <div
          :class="showTwoColumns('correlation')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
            v-if="images.correlation[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div
              v-if="!showTwoColumns('correlation')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.correlation[0]"
                  :key="'rat1-prog1' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div ref="imageViewer" class="flex-shrink-0 max-w-[70%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices4.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index, expandedIndices4, displayedText4, textToDisplay4, typingIntervals4)"
                    >
                      {{ expandedIndices4.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices4.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          {{ displayedText4[index % textToDisplay4.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.correlation[0]"
                  :key="'rat1-col2-' + index"
                  class="border-b pb-4 mb-4"
                >
                 <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Set 2 -->
          <div
            v-if="showSecondOptions.correlation && images.correlation[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <ul>
              <li
                v-for="(image, idx) in images.correlation[1]"
                :key="'corr2-' + idx"
                class="border-b pb-4 mb-4"
              >
                <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>


      <!-- ~~~~~ SECTION V: Brands (UPDATED STYLING) ~~~~~ -->
      <section id="brands" class="mb-12 scroll-mt-20">
        <h1 class="text-2xl font-bold mb-4">V. Brands</h1>
        <p class="text-sm mb-4 text-gray-600">
          Compares brand‐level performance across all rating dimensions.
          A table (top 10 brands) highlights each brand’s scores, with the best values in each column emphasized,
          making it easy to see which labels excel in scent, longevity, price, etc.
        </p>

        <!-- FILTERS -->
        <div class="mb-6 flex flex-col">
          <h2 class="text-xl font-semibold mb-4">Select Filters</h2>

          <!-- First row: Set 1, Compare With, and Set 2 -->
          <div
            class="flex"
            :class="!showSecondOptions.brands
              ? 'items-center space-x-6'
              : 'items-center justify-center gap-x-20'"
          >
            <!-- Set 1 -->
            <div class="flex space-x-4">
              <div class="flex flex-col w-32">
                <label for="brandsDecade1" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.brands.set1.decade"
                  id="brandsDecade1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="brandsGender1" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.brands.set1.gender"
                  id="brandsGender1"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>

            <!-- Compare With button -->
            <div>
              <button
                v-if="!showSecondOptions.brands"
                @click="toggleSecondOptions('brands')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Compare with...
              </button>

              <button
                v-else
                @click="toggleSecondOptions('brands')"
                class="text-[#7EACB5] hover:text-[#FFF4EA] hover:bg-[#7EACB5]
                border-2 py-2 px-4 rounded-md border-[#7EACB5]
                font-bold text-sm focus:outline-none"
              >
                Remove comparison
              </button>
            </div>

            <!-- Set 2 -->
            <div
              v-if="showSecondOptions.brands"
              class="flex space-x-4"
            >
              <div class="flex flex-col w-32">
                <label for="brandsDecade2" class="text-sm font-medium">Decade</label>
                <select
                  v-model="filters.brands.set2.decade"
                  id="brandsDecade2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="1990">1990s</option>
                  <option value="2000">2000s</option>
                  <option value="2010">2010s</option>
                  <option value="2020">2020s</option>
                </select>
              </div>
              <div class="flex flex-col w-32">
                <label for="brandsGender2" class="text-sm font-medium">Gender</label>
                <select
                  v-model="filters.brands.set2.gender"
                  id="brandsGender2"
                  class="mt-1 block rounded-md border-gray-300 shadow-sm focus:ring-indigo-500"
                >
                  <option value="All">All</option>
                  <option value="Masculine">Masculine</option>
                  <option value="Feminine">Feminine</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Fetch button -->
          <div
            class="mt-4"
            :class="!showSecondOptions.brands
              ? 'self-start'
              : 'self-center'"
          >
            <button
              @click="fetchBrands"
              :disabled="loading5"
              class="bg-[#C96868] text-white py-2 px-4 rounded-md
                     hover:bg-[#C45A5A] focus:outline-none focus:ring-2 focus:ring-[#FADFA1]"
            >
              {{loading5 ? "Loading..." : "Get Brands"}}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="error5" class="mt-4 text-red-600 font-medium text-center">
          {{ error5 }}
        </p>

        <!-- DISPLAY IMAGES -->
        <div
          :class="showTwoColumns('brands')
            ? 'grid grid-cols-2 gap-6'
            : 'flex justify-center items-start'"
        >
          <!-- Set 1 -->
          <div
            v-if="images.brands[0]?.length"
            class="flex flex-col w-full mb-4"
          >
            <div
              v-if="!showTwoColumns('brands')"
              class="flex-1 h-full"
            >
              <ul class="space-y-6 px-2">
                <li
                  v-for="(image, index) in images.brands[0]"
                  :key="'rat1-prog1' + index"
                  class="relative flex justify-center items-stretch border-b pb-4 mb-4"
                >
                  <!-- The image -->
                  <div ref="imageViewer" class="flex-shrink-0 max-w-[70%]">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>

                  <!-- Toggle Explanation -->
                  <div
                    class="relative pl-2 transition-all duration-1000"
                    :class="[expandedIndices5.includes(index) ? 'w-80' : 'w-24']"
                  >
                    <div
                      class="sticky top-20 z-10 w-24 h-10 bg-[#C96868] text-white font-bold text-sm
                             rounded shadow-sm flex items-center justify-center
                             cursor-pointer select-none"
                      @click="toggleExplanation(index, expandedIndices5, displayedText5, textToDisplay5, typingIntervals5)"
                    >
                      {{ expandedIndices5.includes(index) ? 'Hide Info' : 'More Info' }}
                    </div>

                    <transition name="fade">
                      <div
                        v-if="expandedIndices5.includes(index)"
                        class="sticky top-32 z-10 bg-white p-4 shadow-md rounded mt-2"
                      >
                        <h3 class="font-bold mb-2">Explanation</h3>
                        <p class="text-sm">
                          {{ displayedText5[index % textToDisplay5.length] }}
                        </p>
                      </div>
                    </transition>
                  </div>
                </li>
              </ul>
            </div>

            <!-- If two columns => just images in a scroll container -->
            <div
              v-else
              class="overflow-y-auto h-full"
            >
              <ul>
                <li
                  v-for="(image, index) in images.brands[0]"
                  :key="'rat1-col2-' + index"
                  class="border-b pb-4 mb-4"
                >
                  <div ref="imageViewer">
                    <img
                      :src="'data:image/png;base64,' + image.base64"
                      alt="Decoded Image"
                      class="w-full h-auto rounded-md shadow-md object-contain"
                    />
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <!-- Set 2 -->
          <div
            v-if="showSecondOptions.brands && images.brands[1]?.length"
            class="flex flex-col w-full mb-4"
          >
            <ul>
              <li
                v-for="(image, idx) in images.brands[1]"
                :key="'brands2-' + idx"
                class="border-b pb-4 mb-4"
              >
                <div ref="imageViewer">
                  <img
                    :src="'data:image/png;base64,' + image.base64"
                    alt="Decoded Image"
                    class="w-full h-auto rounded-md shadow-md object-contain"
                  />
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api"; // or Axios instance / fetch utility

export default {
  name: "FiveSectionFiltersPlusTypewriter",
  data() {
    return {
      loading1: false,
      loading2: false,
      loading3: false,
      loading4: false,
      loading5: false,
      error1: "",
      error2: "",
      error3: "",
      error4: "",
      error5: "",
      showSecondOptions: {
        ratings: false,
        ratingsProgression: false,
        categoriesAndNotes: false,
        correlation: false,
        brands: false,
      },
      textToDisplay: [
        "The first table provides descriptive statistics, including the count, mean, median, mode, and standard deviation for each rating. The second table gives percentile-based distribution (25th, 50th, 75th percentiles) and the minimum and maximum values.",
        "Each box plot visualizes the median, interquartile range (IQR), and overall spread of the data, along with potential outliers (marked as dots). This plot is used to quickly assess the central tendency, variability, and any anomalies in the ratings for each rating.",
        "The QQ plots in this picture are used to assess whether the data for each rating follows a normal distribution by comparing the ordered data values to theoretical quantiles from a normal distribution. If the data points closely follow the red reference line, it suggests that the data is approximately normally distributed. Deviations from the line, particularly at the tails, indicate potential skewness or outliers.",
        "A violin plot combines a box plot and a kernel density plot to display both the distribution and central tendency of the data. The wider sections represent where data points are more concentrated, while the narrower sections indicate less frequent values. The central box plot provides additional insights into the median and interquartile range (IQR).",
        "The image presents a pair plot, which combines histograms and scatter plots to visualize relationships and distributions. The histograms on the diagonal show the distribution of individual ratings, while the scatter plots depict all possible pairwise relationships between the selected ratings. This type of plot is useful for identifying trends, correlations, and patterns across multiple variables.",
      ],
      displayedText: ["", "", "", "", ""], // For Ratings
      textToDisplay2: [
          "The image displays multiple line plots showing the yearly average values for each rating over time, with a shaded region representing the standard deviation of ±1 around each point. The line connects the yearly averages, highlighting trends or fluctuations across the years. The shaded area provides a sense of the variability in the data, with wider regions indicating higher inconsistency among reviews for that year."
      ],
      displayedText2: [""], // For Ratings Progression
      textToDisplay3: [
          "The image consists of multiple pie charts representing the distribution of different fragrance categories, with each slice corresponding to a specific category's percentage contribution. The 'Others' sections in each chart includes categories contributing less than 1% individually. This visualization highlights the diversity of fragrance types and allows for an easy comparison of the relative popularity or occurrence of each category.",
          "The bar chart displays the top 25 most frequently used fragrance notes in the dataset, ranked by the number of perfumes that include each note. The chart highlights the prevalence of certain notes compared to others, providing insight into the most popular ingredients in the dataset."
      ],
      displayedText3: ["", ""], // For Categories & Notes
      textToDisplay4: [
          "The heatmap illustrates the correlation between the available categories and all rating rubrics. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how categories may influence the perceived qualities of a perfume.",
          "The heatmap illustrates the correlation between the top 50 notes and the available categories. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how notes may influence the categories users classify the perfumes in.",
          "The heatmap illustrates the correlation between the top 50 notes and all rating rubrics. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how notes may influence the perceived qualities of a perfume."
      ],
      displayedText4: ["", "", ""], // For Correlation
      textToDisplay5: [
        "The table compares brand performance across all ratings, with the highest value in each column being highlighted. Only the top 10 most frequent brands are displayed. This visualization allows for quick identification of the best-performing brands in specific categories, showcasing their strengths. "
      ],
      displayedText5: [""], // For Brands

      expandedIndices1: [],
      expandedIndices2: [],
      expandedIndices3: [],
      expandedIndices4: [],
      expandedIndices5: [],

      typingIntervals1: {},
      typingIntervals2: {},
      typingIntervals3: {},
      typingIntervals4: {},
      typingIntervals5: {},

      filters: {
        ratings: { set1: { decade: "All", gender: "All" }, set2: { decade: "All", gender: "All" } },
        ratingsProgression: { set1: { decade: "All", gender: "All" }, set2: { decade: "All", gender: "All" } },
        categoriesAndNotes: { set1: { decade: "All", gender: "All" }, set2: { decade: "All", gender: "All" } },
        correlation: { set1: { decade: "All", gender: "All" }, set2: { decade: "All", gender: "All" } },
        brands: { set1: { decade: "All", gender: "All" }, set2: { decade: "All", gender: "All" } },
      },
      images: {
        ratings: [[], []],
        ratingsProgression: [[], []],
        categoriesAndNotes: [[], []],
        correlation: [[], []],
        brands: [[], []],
      },
    };
  },
  methods: {
    typeText(displayedTextArray, fullTextToDisplay, textSlotIndex, sectionTypingIntervalsStore) {
      if (sectionTypingIntervalsStore[textSlotIndex]) {
        clearInterval(sectionTypingIntervalsStore[textSlotIndex]);
      }
      let currentCharacterIndex = 0;
      displayedTextArray[textSlotIndex] = "";
      this.$forceUpdate(); // May be needed if Vue doesn't pick up direct array index modification for reactivity in some cases

      sectionTypingIntervalsStore[textSlotIndex] = setInterval(() => {
        if (currentCharacterIndex < fullTextToDisplay.length) {
          displayedTextArray[textSlotIndex] += fullTextToDisplay[currentCharacterIndex];
          currentCharacterIndex++;
          this.$forceUpdate(); // Ensure reactive update of the text
        } else {
          clearInterval(sectionTypingIntervalsStore[textSlotIndex]);
          delete sectionTypingIntervalsStore[textSlotIndex];
        }
      }, 20);
    },

    toggleExplanation(imageIndex, expandedIndicesArray, displayedTextArray, textToDisplayArray, sectionTypingIntervalsStore) {
      const i = expandedIndicesArray.indexOf(imageIndex);
      const textSlotIndex = imageIndex % textToDisplayArray.length;

      if (i > -1) {
        expandedIndicesArray.splice(i, 1);
        displayedTextArray[textSlotIndex] = "";
        if (sectionTypingIntervalsStore[textSlotIndex]) {
          clearInterval(sectionTypingIntervalsStore[textSlotIndex]);
          delete sectionTypingIntervalsStore[textSlotIndex];
        }
      } else {
        expandedIndicesArray.push(imageIndex);
        this.typeText(
          displayedTextArray,
          textToDisplayArray[textSlotIndex],
          textSlotIndex,
          sectionTypingIntervalsStore
        );
      }
       this.$forceUpdate(); // Ensure overall component reactivity if needed
    },

    toggleSecondOptions(section) {
      this.showSecondOptions[section] = !this.showSecondOptions[section];
      // Note: Changing this does not automatically re-fetch. User needs to click "Get <Section>" again.
      // If re-fetch is desired, call the fetch method here, but be mindful of UX.
    },

    showTwoColumns(section) {
      return (
        this.showSecondOptions[section] &&
        this.images[section] && // ensure images[section] exists
        this.images[section][1] &&
        this.images[section][1].length > 0
      );
    },

    resetSectionState(sectionIndex, textDisplayArrayBase, displayedTextArrayName, expandedIndicesArrayName, typingIntervalsStoreName) {
        this[expandedIndicesArrayName] = [];
        this[displayedTextArrayName] = Array(textDisplayArrayBase.length).fill("");
        if (this[typingIntervalsStoreName]) {
            Object.values(this[typingIntervalsStoreName]).forEach(clearInterval);
        }
        this[typingIntervalsStoreName] = {};
    },

    async fetchRatings() {
      this.error1 = "";
      this.loading1 = true;
      this.resetSectionState(0, this.textToDisplay, 'displayedText', 'expandedIndices1', 'typingIntervals1');

      try {
        const relevantSets = this.showSecondOptions.ratings
          ? [this.filters.ratings.set1, this.filters.ratings.set2]
          : [this.filters.ratings.set1];
        const responses = await Promise.all(
          relevantSets.map((opts) => apiClient.get("/test/eda-ratings", { params: opts }))
        );
        this.images.ratings[0] = responses[0]?.data?.images || [];
        this.images.ratings[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error("Error fetching Ratings data:", err);
        this.error1 = "Error fetching Ratings data. Try refreshing or check console.";
        this.images.ratings = [[],[]]; // Clear on error
      } finally {
        this.loading1 = false;
      }
    },

    async fetchRatingsProgression() {
      this.error2 = "";
      this.loading2 = true;
      this.resetSectionState(1, this.textToDisplay2, 'displayedText2', 'expandedIndices2', 'typingIntervals2');
      try {
        const relevantSets = this.showSecondOptions.ratingsProgression
          ? [ this.filters.ratingsProgression.set1, this.filters.ratingsProgression.set2, ]
          : [this.filters.ratingsProgression.set1];
        const responses = await Promise.all(
          relevantSets.map((opts) => apiClient.get("/test/eda-ratings-prog", { params: opts }))
        );
        this.images.ratingsProgression[0] = responses[0]?.data?.images || [];
        this.images.ratingsProgression[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error("Error fetching Ratings Progression data:", err);
        this.error2 = "Error fetching Ratings progression. Try refreshing or check console.";
        this.images.ratingsProgression = [[],[]];
      } finally {
        this.loading2 = false;
      }
    },

    async fetchCategoriesAndNotes() {
      this.error3 = "";
      this.loading3 = true;
      this.resetSectionState(2, this.textToDisplay3, 'displayedText3', 'expandedIndices3', 'typingIntervals3');
      try {
        const relevantSets = this.showSecondOptions.categoriesAndNotes
          ? [ this.filters.categoriesAndNotes.set1, this.filters.categoriesAndNotes.set2, ]
          : [this.filters.categoriesAndNotes.set1];
        const responses = await Promise.all(
          relevantSets.map((opts) => apiClient.get("/test/eda-cat-notes", { params: opts }))
        );
        this.images.categoriesAndNotes[0] = responses[0]?.data?.images || [];
        this.images.categoriesAndNotes[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error("Error fetching Categories/Notes data:", err);
        this.error3 = "Error fetching Categories & Notes. Try refreshing or check console.";
        this.images.categoriesAndNotes = [[],[]];
      } finally {
        this.loading3 = false;
      }
    },

    async fetchCorrelation() {
      this.error4 = "";
      this.loading4 = true;
      this.resetSectionState(3, this.textToDisplay4, 'displayedText4', 'expandedIndices4', 'typingIntervals4');
      try {
        const relevantSets = this.showSecondOptions.correlation
          ? [this.filters.correlation.set1, this.filters.correlation.set2]
          : [this.filters.correlation.set1];
        const responses = await Promise.all(
          relevantSets.map((opts) => apiClient.get("/test/eda-correlation", { params: opts }))
        );
        this.images.correlation[0] = responses[0]?.data?.images || [];
        this.images.correlation[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error("Error fetching Correlation data:", err);
        this.error4 = "Error fetching Correlation data. Try refreshing or check console.";
        this.images.correlation = [[],[]];
      } finally {
        this.loading4 = false;
      }
    },

    async fetchBrands() {
      this.error5 = "";
      this.loading5 = true;
      this.resetSectionState(4, this.textToDisplay5, 'displayedText5', 'expandedIndices5', 'typingIntervals5');
      try {
        const relevantSets = this.showSecondOptions.brands
          ? [this.filters.brands.set1, this.filters.brands.set2]
          : [this.filters.brands.set1];
        const responses = await Promise.all(
          relevantSets.map((opts) => apiClient.get("/test/eda-brands", { params: opts }))
        );
        this.images.brands[0] = responses[0]?.data?.images || [];
        this.images.brands[1] = responses[1]?.data?.images || [];
      } catch (err) {
        console.error("Error fetching Brands data:", err);
        this.error5 = "Error fetching Brands data. Try refreshing or check console.";
        this.images.brands = [[],[]];
      } finally {
        this.loading5 = false;
      }
    },
  },
};
</script>

<!--<script>-->
<!--import apiClient from "@/api"; // or Axios instance / fetch utility-->

<!--export default {-->
<!--  name: "FiveSectionFiltersPlusTypewriter",-->
<!--  data() {-->
<!--    return {-->
<!--      loading1: false,-->
<!--      loading2: false,-->
<!--      loading3: false,-->
<!--      loading4: false,-->
<!--      loading5: false,-->
<!--      error1: "",-->
<!--      error2: "",-->
<!--      error3: "",-->
<!--      error4: "",-->
<!--      error5: "",-->
<!--      // For toggling second set of filters in each section-->
<!--      showSecondOptions: {-->
<!--        ratings: false,-->
<!--        ratingsProgression: false,-->
<!--        categoriesAndNotes: false,-->
<!--        correlation: false,-->
<!--        brands: false,-->
<!--      },-->
<!--      // The user’s typed text placeholders-->
<!--      textToDisplay: [-->
<!--        "The first table provides descriptive statistics, including the count, mean, median, mode, and standard deviation for each rating. The second table gives percentile-based distribution (25th, 50th, 75th percentiles) and the minimum and maximum values.",-->
<!--        "Each box plot visualizes the median, interquartile range (IQR), and overall spread of the data, along with potential outliers (marked as dots). This plot is used to quickly assess the central tendency, variability, and any anomalies in the ratings for each rating.",-->
<!--        "The image presents a pair plot, which combines histograms and scatter plots to visualize relationships and distributions. The histograms on the diagonal show the distribution of individual ratings, while the scatter plots depict all possible pairwise relationships between the selected ratings. This type of plot is useful for identifying trends, correlations, and patterns across multiple variables.",-->
<!--        "The QQ plots in this picture are used to assess whether the data for each rating follows a normal distribution by comparing the ordered data values to theoretical quantiles from a normal distribution. If the data points closely follow the red reference line, it suggests that the data is approximately normally distributed. Deviations from the line, particularly at the tails, indicate potential skewness or outliers.",-->
<!--        "A violin plot combines a box plot and a kernel density plot to display both the distribution and central tendency of the data. The wider sections represent where data points are more concentrated, while the narrower sections indicate less frequent values. The central box plot provides additional insights into the median and interquartile range (IQR).",-->
<!--      ],-->
<!--      // Where typed text is displayed-->
<!--      displayedText: ["", "", "", "", ""],-->
<!--      textToDisplay2: [-->
<!--          "The image displays multiple line plots showing the yearly average values for each rating over time, with a shaded region representing the standard deviation of ±1 around each point. The line connects the yearly averages, highlighting trends or fluctuations across the years. The shaded area provides a sense of the variability in the data, with wider regions indicating higher inconsistency among reviews for that year."-->
<!--      ],-->
<!--      displayedText2: [""],-->
<!--      textToDisplay3: [-->
<!--          "The image consists of multiple pie charts representing the distribution of different fragrance categories, with each slice corresponding to a specific category's percentage contribution. The 'Others' sections in each chart includes categories contributing less than 1% individually. This visualization highlights the diversity of fragrance types and allows for an easy comparison of the relative popularity or occurrence of each category.",-->
<!--          "The bar chart displays the top 25 most frequently used fragrance notes in the dataset, ranked by the number of perfumes that include each note. The chart highlights the prevalence of certain notes compared to others, providing insight into the most popular ingredients in the dataset."-->
<!--      ],-->
<!--      displayedText3: ["", ""],-->
<!--      textToDisplay4: [-->
<!--          "The heatmap illustrates the correlation between the available categories and all rating rubrics. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how categories may influence the perceived qualities of a perfume.",-->
<!--          "The heatmap illustrates the correlation between the top 50 notes and the available categories. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how notes may influence the categories users classify the perfumes in.",-->
<!--          "The heatmap illustrates the correlation between the top 50 notes and all rating rubrics. Each cell's color intensity indicates the strength and direction of the correlation, with a gradient ranging from negative (blue) to positive (red). This visualization provides a comprehensive overview of how notes may influence the perceived qualities of a perfume."-->
<!--      ],-->
<!--      displayedText4: ["", "", ""],-->
<!--      textToDisplay5: [-->
<!--        "The table compares brand performance across all ratings, with the highest value in each column being highlighted. Only the top 10 most frequent brands are displayed. This visualization allows for quick identification of the best-performing brands in specific categories, showcasing their strengths. "-->
<!--      ],-->
<!--      displayedText5: [""],-->
<!--      // Indices for which images are expanded (for single-col scenario)-->
<!--      expandedIndices1: [],-->
<!--      expandedIndices2: [],-->
<!--      expandedIndices3: [],-->
<!--      expandedIndices4: [],-->
<!--      expandedIndices5: [],-->

<!--      // Each section has 2 sets of filters (like original code).-->
<!--      filters: {-->
<!--        ratings: {-->
<!--          set1: { decade: "All", gender: "All" },-->
<!--          set2: { decade: "All", gender: "All" },-->
<!--        },-->
<!--        ratingsProgression: {-->
<!--          set1: { decade: "All", gender: "All" },-->
<!--          set2: { decade: "All", gender: "All" },-->
<!--        },-->
<!--        categoriesAndNotes: {-->
<!--          set1: { decade: "All", gender: "All" },-->
<!--          set2: { decade: "All", gender: "All" },-->
<!--        },-->
<!--        correlation: {-->
<!--          set1: { decade: "All", gender: "All" },-->
<!--          set2: { decade: "All", gender: "All" },-->
<!--        },-->
<!--        brands: {-->
<!--          set1: { decade: "All", gender: "All" },-->
<!--          set2: { decade: "All", gender: "All" },-->
<!--        },-->
<!--      },-->

<!--      // Each section now stores up to 2 arrays of images-->
<!--      images: {-->
<!--        ratings: [[], []],-->
<!--        ratingsProgression: [[], []],-->
<!--        categoriesAndNotes: [[], []],-->
<!--        correlation: [[], []],-->
<!--        brands: [[], []],-->
<!--      },-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    // === TYPEWRITER METHOD ===-->
<!--    typeText(dT, textPremade, textIndex) {-->
<!--      let index = 0;-->

<!--      // Reset displayed text if previously typed-->
<!--      if (dT[textIndex] !== "") {-->
<!--        dT[textIndex] = "";-->
<!--      }-->

<!--      const interval = setInterval(() => {-->
<!--        if (index < textPremade.length) {-->
<!--          dT[textIndex] += textPremade[index];-->
<!--          index++;-->
<!--        } else {-->
<!--          clearInterval(interval); // Stop when text is fully typed-->
<!--        }-->
<!--      }, 20);-->
<!--    },-->

<!--    // === TOGGLE EXPLANATION (SINGLE-COL ONLY) ===-->
<!--    toggleExplanation(index, eI, dT, ttD) {-->
<!--      const i = eI.indexOf(index);-->
<!--      if (i > -1) {-->
<!--        // Already expanded => collapse-->
<!--        eI.splice(i, 1);-->
<!--        // Clear typed text-->
<!--        dT[index % ttD.length] = "";-->
<!--      } else {-->
<!--        // Expand-->
<!--        eI.push(index);-->
<!--        // Trigger typewriter for that index-->
<!--        this.typeText(-->
<!--            dT,-->
<!--          ttD[index % ttD.length],-->
<!--          index % ttD.length-->
<!--        );-->
<!--      }-->
<!--    },-->

<!--    // === TOGGLE SECOND SET OF FILTERS (COMPARE WITH) ===-->
<!--    toggleSecondOptions(section) {-->
<!--      this.showSecondOptions[section] = !this.showSecondOptions[section];-->
<!--    },-->

<!--    // === CHECK IF WE SHOW 2 COLUMNS OF IMAGES ===-->
<!--    showTwoColumns(section) {-->
<!--      return (-->
<!--        this.showSecondOptions[section] &&-->
<!--        this.images[section][1] &&-->
<!--        this.images[section][1].length > 0-->
<!--      );-->
<!--    },-->

<!--    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-->
<!--    // All the "fetch" methods: each makes 1 or 2 API calls-->
<!--    // depending on whether second set is toggled-->
<!--    // ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-->
<!--    async fetchRatings() {-->
<!--      this.error1 = "";-->

<!--      this.loading1 = true;-->

<!--      try {-->
<!--        // Build an array of sets to fetch-->
<!--        const relevantSets = this.showSecondOptions.ratings-->
<!--          ? [this.filters.ratings.set1, this.filters.ratings.set2]-->
<!--          : [this.filters.ratings.set1];-->

<!--        // Make parallel calls-->
<!--        const responses = await Promise.all(-->
<!--          relevantSets.map((opts) =>-->
<!--            apiClient.get("/test/eda-ratings", {-->
<!--              params: {-->
<!--                decade: opts.decade,-->
<!--                gender: opts.gender,-->
<!--              },-->
<!--            })-->
<!--          )-->
<!--        );-->

<!--        // Store into images.ratings[0] and [1]-->
<!--        this.images.ratings[0] = responses[0].data.images || [];-->
<!--        this.images.ratings[1] = responses[1]?.data?.images || [];-->
<!--        this.expandedIndices = []; // reset expansions-->

<!--        this.loading1 = false;-->
<!--      } catch (err) {-->
<!--        console.error(err);-->
<!--        this.error1 = "Error fetching Ratings data. Try refreshing the page";-->
<!--      }-->
<!--    },-->

<!--    async fetchRatingsProgression() {-->
<!--      this.error2 = "";-->
<!--      this.loading2 = true;-->

<!--      try {-->
<!--        const relevantSets = this.showSecondOptions.ratingsProgression-->
<!--          ? [-->
<!--              this.filters.ratingsProgression.set1,-->
<!--              this.filters.ratingsProgression.set2,-->
<!--            ]-->
<!--          : [this.filters.ratingsProgression.set1];-->

<!--        const responses = await Promise.all(-->
<!--          relevantSets.map((opts) =>-->
<!--            apiClient.get("/test/eda-ratings-prog", {-->
<!--              params: {-->
<!--                decade: opts.decade,-->
<!--                gender: opts.gender,-->
<!--              },-->
<!--            })-->
<!--          )-->
<!--        );-->

<!--        this.images.ratingsProgression[0] = responses[0].data.images || [];-->
<!--        this.images.ratingsProgression[1] = responses[1]?.data?.images || [];-->

<!--        this.loading2 = false;-->
<!--      } catch (err) {-->
<!--        console.error(err);-->
<!--        this.error2 = "Error fetching Ratings progression data. Try refreshing the page";-->
<!--      }-->
<!--    },-->

<!--    async fetchCategoriesAndNotes() {-->
<!--      this.error3 = "";-->
<!--      this.loading3 = true;-->

<!--      try {-->
<!--        const relevantSets = this.showSecondOptions.categoriesAndNotes-->
<!--          ? [-->
<!--              this.filters.categoriesAndNotes.set1,-->
<!--              this.filters.categoriesAndNotes.set2,-->
<!--            ]-->
<!--          : [this.filters.categoriesAndNotes.set1];-->

<!--        const responses = await Promise.all(-->
<!--          relevantSets.map((opts) =>-->
<!--            apiClient.get("/test/eda-cat-notes", {-->
<!--              params: {-->
<!--                decade: opts.decade,-->
<!--                gender: opts.gender,-->
<!--              },-->
<!--            })-->
<!--          )-->
<!--        );-->

<!--        this.images.categoriesAndNotes[0] = responses[0].data.images || [];-->
<!--        this.images.categoriesAndNotes[1] = responses[1]?.data?.images || [];-->

<!--        this.loading3 = false;-->
<!--      } catch (err) {-->
<!--        console.error(err);-->
<!--        this.error3 = "Error fetching Categories & Notes data. Try refreshing the page";-->
<!--      }-->
<!--    },-->

<!--    async fetchCorrelation() {-->
<!--      this.error4 = "";-->
<!--      this.loading4 = true;-->

<!--      try {-->
<!--        const relevantSets = this.showSecondOptions.correlation-->
<!--          ? [this.filters.correlation.set1, this.filters.correlation.set2]-->
<!--          : [this.filters.correlation.set1];-->

<!--        const responses = await Promise.all(-->
<!--          relevantSets.map((opts) =>-->
<!--            apiClient.get("/test/eda-correlation", {-->
<!--              params: {-->
<!--                decade: opts.decade,-->
<!--                gender: opts.gender,-->
<!--              },-->
<!--            })-->
<!--          )-->
<!--        );-->

<!--        this.images.correlation[0] = responses[0].data.images || [];-->
<!--        this.images.correlation[1] = responses[1]?.data?.images || [];-->

<!--        this.loading4 = false;-->
<!--      } catch (err) {-->
<!--        console.error(err);-->
<!--        this.error4 = "Error fetching Correlation data. Try refreshing the page";-->
<!--      }-->
<!--    },-->

<!--    async fetchBrands() {-->
<!--      this.error5 = "";-->
<!--      this.loading5 = true;-->

<!--      try {-->
<!--        const relevantSets = this.showSecondOptions.brands-->
<!--          ? [this.filters.brands.set1, this.filters.brands.set2]-->
<!--          : [this.filters.brands.set1];-->

<!--        const responses = await Promise.all(-->
<!--          relevantSets.map((opts) =>-->
<!--            apiClient.get("/test/eda-brands", {-->
<!--              params: {-->
<!--                decade: opts.decade,-->
<!--                gender: opts.gender,-->
<!--              },-->
<!--            })-->
<!--          )-->
<!--        );-->

<!--        this.images.brands[0] = responses[0].data.images || [];-->
<!--        this.images.brands[1] = responses[1]?.data?.images || [];-->
<!--        this.loading5 = false;-->
<!--      } catch (err) {-->
<!--        console.error(err);-->
<!--        this.error5 = "Error fetching Brands data.mTry refreshing the page";-->
<!--      }-->
<!--    },-->
<!--  },-->
<!--};-->
<!--</script>-->

<style scoped>

/* Fade transition for typed explanation box */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Example sticky sidebar ensuring full height */
aside {
  min-height: 100vh;
}
</style>
