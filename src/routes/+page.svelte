<script>
	import { onMount } from 'svelte';

	let gigs = [];
	let searchQuery = '';
	let selectedSubreddit = 'ALL';
	let isLoading = false;

	async function loadGigs() {
		isLoading = true;
		try {
			const res = await fetch('/api/gigs');
			if (res.ok) {
				gigs = await res.json();
			}
		} catch (e) {
			console.error('Feed Sync Error:', e);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		loadGigs();
	});

	$: filteredGigs = gigs.filter((gig) => {
		const matchesSearch = gig.title?.toLowerCase().includes(searchQuery.toLowerCase());
		const matchesSub =
			selectedSubreddit === 'ALL' ||
			gig.subreddit?.toLowerCase() === selectedSubreddit.toLowerCase();
		return matchesSearch && matchesSub;
	});

	function formatTimestamp(utcSeconds) {
		if (!utcSeconds) return '-';
		const date = new Date(utcSeconds * 1000);
		return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + ' // ' + 
			   date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
	}
</script>

<svelte:head>
	<title>GIG DIRECTORY</title>
	<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;700&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
</svelte:head>

<div class="app-container">
	<header class="top-nav">
		<div class="brand">
			<div class="accent-box"></div>
			<h1>GIG DIRECTORY</h1>
		</div>
		<div class="record-count">
			{filteredGigs.length} {filteredGigs.length === 1 ? 'MATCH' : 'MATCHES'}
		</div>
	</header>

	<main class="content-wrapper">
		<div class="controls-container">
			<div class="input-group">
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search listings..."
					class="v-input"
				/>
			</div>

			<div class="input-group">
				<select bind:value={selectedSubreddit} class="v-select">
					<option value="ALL">ALL SUBREDDITS</option>
					<option value="slavelabour">r/slavelabour</option>
					<option value="doneDirtCheap">r/doneDirtCheap</option>
					<option value="forhire">r/forhire</option>
				</select>
			</div>

			<button class="v-btn" on:click={loadGigs} disabled={isLoading}>
				{isLoading ? 'SYNCING...' : 'REFRESH'}
			</button>
		</div>

		<div class="table-wrapper">
			<table class="v-table">
				<thead>
					<tr>
						<th class="col-time">POSTED</th>
						<th class="col-sub">SOURCE</th>
						<th class="col-title">LISTING DETAILS</th>
						<th class="col-action"></th>
					</tr>
				</thead>
				<tbody>
					{#if filteredGigs.length === 0}
						<tr class="empty-state">
							<td colspan="4">
								{#if isLoading}
									LOADING DATA...
								{:else}
									NO LISTINGS MATCH YOUR CRITERIA
								{/if}
							</td>
						</tr>
					{:else}
						{#each filteredGigs as gig}
							<tr>
								<td class="col-time">{formatTimestamp(gig.created)}</td>
								<td class="col-sub"><span class="badge">{gig.subreddit}</span></td>
								<td class="col-title">{gig.title}</td>
								<td class="col-action">
									<a href={gig.link} target="_blank" rel="noreferrer" class="link-btn">VIEW</a>
								</td>
							</tr>
						{/each}
					{/if}
				</tbody>
			</table>
		</div>
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		background-color: #0f1923;
		color: #ece8e1;
		font-family: 'Barlow', system-ui, -apple-system, sans-serif;
		-webkit-font-smoothing: antialiased;
	}

	.app-container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 2rem;
	}

	.top-nav {
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		border-bottom: 1px solid #282c31;
		padding-bottom: 1rem;
		margin-bottom: 2rem;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.accent-box {
		width: 12px;
		height: 12px;
		background-color: #ff4655;
	}

	h1 {
		margin: 0;
		font-family: 'Oswald', sans-serif;
		font-size: 2.5rem;
		font-weight: 700;
		letter-spacing: 2px;
		line-height: 1;
		color: #ece8e1;
	}

	.record-count {
		font-family: 'Oswald', sans-serif;
		font-size: 1.25rem;
		color: #768079;
		letter-spacing: 1px;
	}

	.controls-container {
		display: flex;
		gap: 1rem;
		margin-bottom: 1.5rem;
	}

	.input-group {
		flex: 1;
		position: relative;
	}

	.v-input, .v-select {
		width: 100%;
		background-color: rgba(255, 255, 255, 0.05);
		border: 1px solid #282c31;
		color: #ece8e1;
		padding: 0.75rem 1rem;
		font-family: 'Barlow', sans-serif;
		font-size: 1rem;
		font-weight: 500;
		outline: none;
		transition: all 0.2s ease;
		box-sizing: border-box;
	}

	.v-input:focus, .v-select:focus {
		border-color: #ff4655;
		background-color: rgba(255, 70, 85, 0.05);
	}

	.v-btn {
		background-color: #ff4655;
		color: #ece8e1;
		border: 1px solid #ff4655;
		padding: 0 2rem;
		font-family: 'Oswald', sans-serif;
		font-size: 1.1rem;
		font-weight: 500;
		letter-spacing: 1px;
		cursor: pointer;
		transition: all 0.15s ease;
		min-width: 140px;
	}

	.v-btn:hover:not(:disabled) {
		background-color: #ece8e1;
		border-color: #ece8e1;
		color: #0f1923;
	}

	.v-btn:disabled {
		background-color: #282c31;
		border-color: #282c31;
		color: #768079;
		cursor: not-allowed;
	}

	.table-wrapper {
		background-color: rgba(255, 255, 255, 0.02);
		border: 1px solid #282c31;
	}

	.v-table {
		width: 100%;
		border-collapse: collapse;
		text-align: left;
	}

	.v-table th {
		font-family: 'Oswald', sans-serif;
		font-size: 0.9rem;
		font-weight: 500;
		color: #768079;
		letter-spacing: 1px;
		padding: 1rem;
		border-bottom: 1px solid #282c31;
	}

	.v-table td {
		padding: 1rem;
		border-bottom: 1px solid #1f2326;
		transition: background-color 0.15s ease;
	}

	.v-table tbody tr {
		position: relative;
	}

	.v-table tbody tr:hover td {
		background-color: rgba(255, 255, 255, 0.04);
	}

	.v-table tbody tr::before {
		content: '';
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
		width: 3px;
		background-color: #ff4655;
		opacity: 0;
		transition: opacity 0.15s ease;
	}

	.v-table tbody tr:hover::before {
		opacity: 1;
	}

	.col-time {
		width: 160px;
		color: #768079;
		font-size: 0.9rem;
	}

	.col-sub {
		width: 140px;
	}

	.badge {
		display: inline-block;
		background-color: #282c31;
		color: #ece8e1;
		padding: 0.25rem 0.5rem;
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.5px;
		text-transform: uppercase;
	}

	.col-title {
		font-weight: 500;
		font-size: 1.05rem;
	}

	.col-action {
		width: 100px;
		text-align: right;
	}

	.link-btn {
		display: inline-block;
		color: #ff4655;
		text-decoration: none;
		font-family: 'Oswald', sans-serif;
		font-size: 1rem;
		font-weight: 500;
		letter-spacing: 1px;
		padding: 0.25rem 0.5rem;
		border: 1px solid transparent;
		transition: all 0.15s ease;
	}

	.link-btn:hover {
		border-color: #ff4655;
		background-color: rgba(255, 70, 85, 0.1);
	}

	.empty-state td {
		text-align: center;
		padding: 4rem 1rem !important;
		color: #768079;
		font-family: 'Oswald', sans-serif;
		font-size: 1.25rem;
		letter-spacing: 1px;
	}
</style>