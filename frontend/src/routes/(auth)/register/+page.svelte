<script>
  import { authStore } from '$lib/stores/auth.js';
  import { goto } from '$app/navigation';
  
  let email = '';
  let password = '';
  let fullName = '';
  let confirmPassword = '';
  let isLoading = false;
  let error = '';

  async function handleRegister() {
    if (!email || !password || !fullName) {
      error = 'All fields are required';
      return;
    }

    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    if (password.length < 6) {
      error = 'Password must be at least 6 characters';
      return;
    }

    isLoading = true;
    error = '';

    try {
      await authStore.register(email, password, fullName);
      goto('/campaigns');
    } catch (err) {
      error = err.message || 'Registration failed';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen flex items-center justify-center">
  <div class="max-w-md w-full space-y-8">
    <div class="text-center">
      <h2 class="text-3xl font-bold text-gray-900">
        Create your account
      </h2>
      <p class="mt-2 text-sm text-gray-600">
        Or 
        <a href="/login" class="font-medium text-primary-600 hover:text-primary-500">
          sign in to existing account
        </a>
      </p>
    </div>
    
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleRegister}>
      <div class="space-y-4">
        <div>
          <label for="fullName" class="block text-sm font-medium text-gray-700">
            Full Name
          </label>
          <input
            id="fullName"
            type="text"
            bind:value={fullName}
            class="input mt-1"
            placeholder="Enter your full name"
            required
          />
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Email address
          </label>
          <input
            id="email"
            type="email"
            bind:value={email}
            class="input mt-1"
            placeholder="Enter your email"
            required
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            id="password"
            type="password"
            bind:value={password}
            class="input mt-1"
            placeholder="Enter your password"
            required
          />
        </div>
        
        <div>
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            type="password"
            bind:value={confirmPassword}
            class="input mt-1"
            placeholder="Confirm your password"
            required
          />
        </div>
      </div>

      {#if error}
        <div class="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      {/if}

      <button
        type="submit"
        disabled={isLoading}
        class="btn btn-primary w-full"
      >
        {isLoading ? 'Creating account...' : 'Create account'}
      </button>
    </form>
  </div>
</div>