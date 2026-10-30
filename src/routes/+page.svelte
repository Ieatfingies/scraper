<script lang="ts">
	import { onMount } from 'svelte';

	interface Gig {
		id: string;
		title: string;
		link: string;
		subreddit: string;
		created: number;
	}

	let gigs: Gig[] = [];
	let loading = true;

	async function fetchGigs() {
		loading = true;
		try {
			const res = await fetch('/api/gigs');
			if (res.ok) {
				gigs = await res.json();
			}
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchGigs();
	});

	function formatTime(timestamp: number) {
		if (!timestamp) return 'JUST NOW';
		const date = new Date(timestamp * 1000);
		return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}
</script>

<div class="val-bg min-h-screen text-slate-100 font-mono p-4 md:p-8 selection:bg-[#ff4655] selection:text-white">
	<!-- Background Tactical Grid -->
	<div class="fixed inset-0 bg-grid opacity-20 pointer-events-none"></div>

	<main class="max-w-6xl mx-auto relative z-10">
		<!-- Header Banner -->
		<header class="flex flex-col md:flex-row md:items-center justify-between border-b-2 border-slate-800 pb-6 mb-8 gap-4">
			<div>
				<div class="flex items-center gap-3 mb-1">
					<span class="inline-block w-3 h-3 bg-[#ff4655] animate-ping rounded-full"></span>
					<span class="text-xs uppercase tracking-widest text-[#ff4655] font-bold">// SYSTEM PROTOCOL ACTIVE</span>
				</div>
				<h1 class="text-4xl md:text-5xl font-black tracking-tighter uppercase italic text-white flex items-center gap-2">
					REDDIT <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#ff4655] to-[#ff7373]">HUB</span>
				</h1>
			</div>

			<!-- Tactically Styled Refresh Button -->
			<button 
				on:click={fetchGigs} 
				disabled={loading}
				class="val-btn relative group overflow-hidden bg-[#ff4655] text-white px-8 py-3 font-extrabold uppercase tracking-wider text-sm transition-all duration-200 active:scale-95 disabled:opacity-50"
			>
				<span class="relative z-10 flex items-center gap-2">
					{#if loading}
						<svg class="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
						</svg>
						REFRESHING...
					{:else}
						⚡ REFRESH FEED
					{/if}
				</span>
				<!-- Hover Sheen Effect -->
				<div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-500 ease-out"></div>
			</button>
		</header>

		<!-- Feed Area -->
		{#if loading && gigs.length === 0}
			<div class="grid gap-4">
				{#each Array(5) as _}
					<div class="h-24 bg-slate-900/60 border border-slate-800 animate-pulse clip-corners"></div>
				{/each}
			</div>
		{:else if gigs.length === 0}
			<div class="text-center py-20 border border-dashed border-slate-800 rounded">
				<p class="text-slate-500 tracking-widest uppercase">// NO TARGET GIGS DETECTED YET //</p>
			</div>
		{:else}
			<div class="grid gap-4">
				{#each gigs as gig, i (gig.id)}
					<div 
						style="--i: {i}"
						class="val-card group relative bg-slate-900/80 border border-slate-800 hover:border-[#ff4655] p-5 transition-all duration-200 hover:-translate-y-1 hover:shadow-[0_0_20px_rgba(255,70,85,0.25)] flex flex-col md:flex-row md:items-center justify-between gap-4"
					>
						<!-- Left Side Details -->
						<div class="space-y-2 max-w-3xl">
							<div class="flex items-center gap-3">
								<span class="text-[10px] font-bold px-2 py-0.5 bg-slate-800 text-[#ff4655] uppercase tracking-wider border border-[#ff4655]/30">
									r/{gig.subreddit}
								</span>
								<span class="text-xs text-slate-500">
									{formatTime(gig.created)}
								</span>
							</div>
							<h2 class="text-lg font-bold text-slate-100 group-hover:text-white transition-colors leading-snug">
								{gig.title}
							</h2>
						</div>

						<!-- Action Cut-Corner Button -->
						<a 
							href={gig.link} 
							target="_blank" 
							rel="noopener noreferrer"
							class="val-btn-outline group/btn relative inline-flex items-center justify-center px-6 py-2.5 text-xs font-black tracking-widest uppercase text-slate-200 border border-slate-700 group-hover:border-[#ff4655] group-hover:text-white transition-all overflow-hidden shrink-0"
						>
							<span class="relative z-10 flex items-center gap-2">
								VIEW TASK
								<span class="group-hover/btn:translate-x-1 transition-transform">→</span>
							</span>
							<div class="absolute inset-0 bg-[#ff4655] translate-y-full group-hover/btn:translate-y-0 transition-transform duration-200 ease-out"></div>
						</a>
					</div>
				{/each}
			</div>
		{/if}
	</main>
</div>

<style>
	/* Dark Valorant-style background setup */
	.val-bg {
		background-color: #0f1722;
	}

	.bg-grid {
		background-size: 30px 30px;
		background-image: 
			linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
			linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
	}

	/* Tactical Cut Corner Polygon */
	.val-btn, .val-card, .clip-corners {
		clip-path: polygon(
			12px 0, 
			100% 0, 
			100% calc(100% - 12px), 
			calc(100% - 12px) 100%, 
			0 100%, 
			0 12px
		);
	}

	/* Staggered Card Entrance Keyframe */
	.val-card {
		animation: valEnter 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
		animation-delay: calc(var(--i) * 40ms);
		opacity: 0;
		transform: translateY(15px);
	}

	@keyframes valEnter {
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>