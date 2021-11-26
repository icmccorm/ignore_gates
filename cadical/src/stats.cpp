// vim: set tw=300: set VIM text width to 300 characters for this file.

#include "internal.hpp"

namespace CaDiCaL {

/*------------------------------------------------------------------------*/

Stats::Stats () {
  memset (this, 0, sizeof *this);
  time.real = absolute_real_time ();
  time.process = absolute_process_time ();
  walk.minimum = LONG_MAX;
}

/*------------------------------------------------------------------------*/

#define PRT(FMT,...) \
do { \
  if (FMT[0] == ' ' && !all) break; \
  MSG (FMT, __VA_ARGS__); \
} while (0)

/*------------------------------------------------------------------------*/

void Stats::print (Internal * internal) {


  Stats & stats = internal->stats;

  int all = internal->opts.verbose > 0;
#ifdef LOGGING
  if (internal->opts.log) all = true;
#endif // ifdef LOGGING

  if (internal->opts.profile) internal->print_profile ();

  double t = internal->solve_time ();

  int64_t propagations = 0;
  propagations += stats.propagations.cover;
  propagations += stats.propagations.probe;
  propagations += stats.propagations.search;
  propagations += stats.propagations.transred;
  propagations += stats.propagations.vivify;
  propagations += stats.propagations.walk;

  int64_t vivified = stats.vivifysubs + stats.vivifystrs;

  size_t extendbytes = internal->external->extension.size ();
  extendbytes *= sizeof (int);

  printf ("statistics\n");

  if (all || stats.blocked) {
  printf ("blocked:         %15" PRId64 "   %10.2f %%  of irredundant clauses\n", stats.blocked, percent (stats.blocked, stats.added.irredundant));
  printf ("  blockings:     %15" PRId64 "   %10.2f    internal\n", stats.blockings, relative (stats.conflicts, stats.blockings));
  printf ("  candidates:    %15" PRId64 "   %10.2f    per blocking \n", stats.blockcands, relative (stats.blockcands, stats.blockings));
  printf ("  blockres:      %15" PRId64 "   %10.2f    per candidate\n", stats.blockres, relative (stats.blockres, stats.blockcands));
  printf ("  pure:          %15" PRId64 "   %10.2f %%  of all variables\n", stats.all.pure, percent (stats.all.pure, stats.vars));
  printf ("  pureclauses:   %15" PRId64 "   %10.2f    per pure literal\n", stats.blockpured, relative (stats.blockpured, stats.all.pure));
  }
  if (all || stats.chrono)
  printf ("chronological:   %15" PRId64 "   %10.2f %%  of conflicts\n", stats.chrono, percent (stats.chrono, stats.conflicts));
  if (all)
  printf ("compacts:        %15" PRId64 "   %10.2f    interval\n", stats.compacts, relative (stats.conflicts, stats.compacts));
  if (all || stats.conflicts) {
  printf ("conflicts:       %15" PRId64 "   %10.2f    per second\n", stats.conflicts, relative (stats.conflicts, t));
  printf ("  backtracked:   %15" PRId64 "   %10.2f %%  of conflicts\n", stats.backtracks, percent (stats.backtracks, stats.conflicts));
  }
  if (all || stats.conditioned) {
  printf ("conditioned:     %15" PRId64 "   %10.2f %%  of irredundant clauses\n", stats.conditioned, percent (stats.conditioned, stats.added.irredundant));
  printf ("  conditionings: %15" PRId64 "   %10.2f    interval\n", stats.conditionings, relative (stats.conflicts, stats.conditionings));
  printf ("  condcands:     %15" PRId64 "   %10.2f    candidate clauses\n", stats.condcands, relative (stats.condcands, stats.conditionings));
  printf ("  condassinit:   %17.1f  %9.2f %%  initial assigned\n", relative (stats.condassinit, stats.conditionings), percent (stats.condassinit, stats.condassvars));
  printf ("  condcondinit:  %17.1f  %9.2f %%  initial condition\n", relative (stats.condcondinit, stats.conditionings), percent (stats.condcondinit, stats.condassinit));
  printf ("  condautinit:   %17.1f  %9.2f %%  initial autarky\n", relative (stats.condautinit, stats.conditionings), percent (stats.condautinit, stats.condassinit));
  printf ("  condassrem:    %17.1f  %9.2f %%  final assigned\n", relative (stats.condassrem, stats.conditioned), percent (stats.condassrem, stats.condassirem));
  printf ("  condcondrem:   %19.3f  %7.2f %%  final conditional\n", relative (stats.condcondrem, stats.conditioned), percent (stats.condcondrem, stats.condassrem));
  printf ("  condautrem:    %19.3f  %7.2f %%  final autarky\n", relative (stats.condautrem, stats.conditioned), percent (stats.condautrem, stats.condassrem));
  printf ("  condprops:     %15" PRId64 "   %10.2f    per candidate\n", stats.condprops, relative (stats.condprops, stats.condcands));
  }
  if (all || stats.cover.total) {
  printf ("covered:         %15" PRId64 "   %10.2f %%  of irredundant clauses\n", stats.cover.total, percent (stats.cover.total, stats.added.irredundant));
  printf ("  coverings:     %15" PRId64 "   %10.2f    interval\n", stats.cover.count, relative (stats.conflicts, stats.cover.count));
  printf ("  asymmetric:    %15" PRId64 "   %10.2f %%  of covered clauses\n", stats.cover.asymmetric, percent (stats.cover.asymmetric, stats.cover.total));
  printf ("  blocked:       %15" PRId64 "   %10.2f %%  of covered clauses\n", stats.cover.blocked, percent (stats.cover.blocked, stats.cover.total));
  }
  if (all || stats.decisions) {
  printf ("decisions:       %15" PRId64 "   %10.2f    per second\n", stats.decisions, relative (stats.decisions, t));
  printf ("  searched:      %15" PRId64 "   %10.2f    per decision\n", stats.searched, relative (stats.searched, stats.decisions));
  }
  if (all || stats.all.eliminated) {
  printf ("eliminated:      %15" PRId64 "   %10.2f %%  of all variables\n", stats.all.eliminated, percent (stats.all.eliminated, stats.vars));
  printf ("  elimphases:    %15" PRId64 "   %10.2f    interval\n", stats.elimphases, relative (stats.conflicts, stats.elimphases));
  printf ("  elimrounds:    %15" PRId64 "   %10.2f    per phase\n", stats.elimrounds, relative (stats.elimrounds, stats.elimphases));
  printf ("  elimtried:     %15" PRId64 "   %10.2f %%  eliminated\n", stats.elimtried, percent (stats.all.eliminated, stats.elimtried));
  printf ("  elimgates:     %15" PRId64 "   %10.2f %%  gates per tried\n", stats.elimgates, percent (stats.elimgates, stats.elimtried));
  printf ("  elimequivs:    %15" PRId64 "   %10.2f %%  equivalence gates\n", stats.elimequivs, percent (stats.elimequivs, stats.elimgates));
  printf ("  elimands:      %15" PRId64 "   %10.2f %%  and gates\n", stats.elimands, percent (stats.elimands, stats.elimgates));
  printf ("  elimites:      %15" PRId64 "   %10.2f %%  if-then-else gates\n", stats.elimites, percent (stats.elimites, stats.elimgates));
  printf ("  elimxors:      %15" PRId64 "   %10.2f %%  xor gates\n", stats.elimxors, percent (stats.elimxors, stats.elimgates));
  printf ("  elimsubst:     %15" PRId64 "   %10.2f %%  substituted\n", stats.elimsubst, percent (stats.elimsubst, stats.all.eliminated));
  printf ("  elimres:       %15" PRId64 "   %10.2f    per eliminated\n", stats.elimres, relative (stats.elimres, stats.all.eliminated));
  printf ("  elimrestried:  %15" PRId64 "   %10.2f %%  per resolution\n", stats.elimrestried, percent (stats.elimrestried, stats.elimres));
  }
  if (all || stats.all.fixed) {
  printf ("fixed:           %15" PRId64 "   %10.2f %%  of all variables\n", stats.all.fixed, percent (stats.all.fixed, stats.vars));
  printf ("  failed:        %15" PRId64 "   %10.2f %%  of all variables\n", stats.failed, percent (stats.failed, stats.vars));
  printf ("  probefailed:   %15" PRId64 "   %10.2f %%  per failed\n", stats.probefailed, percent (stats.probefailed, stats.failed));
  printf ("  transredunits: %15" PRId64 "   %10.2f %%  per failed\n", stats.transredunits, percent (stats.transredunits, stats.failed));
  printf ("  probingphases: %15" PRId64 "   %10.2f    interval\n", stats.probingphases, relative (stats.conflicts, stats.probingphases));
  printf ("  probesuccess:  %15" PRId64 "   %10.2f %%  phases\n", stats.probesuccess, percent (stats.probesuccess, stats.probingphases));
  printf ("  probingrounds: %15" PRId64 "   %10.2f    per phase\n", stats.probingrounds, relative (stats.probingrounds, stats.probingphases));
  printf ("  probed:        %15" PRId64 "   %10.2f    per failed\n", stats.probed, relative (stats.probed, stats.failed));
  printf ("  hbrs:          %15" PRId64 "   %10.2f    per probed\n", stats.hbrs, relative (stats.hbrs, stats.probed));
  printf ("  hbrsizes:      %15" PRId64 "   %10.2f    per hbr\n", stats.hbrsizes, relative (stats.hbrsizes, stats.hbrs));
  printf ("  hbreds:        %15" PRId64 "   %10.2f %%  per hbr\n", stats.hbreds, percent (stats.hbreds, stats.hbrs));
  printf ("  hbrsubs:       %15" PRId64 "   %10.2f %%  per hbr\n", stats.hbrsubs, percent (stats.hbrsubs, stats.hbrs));
  }
  printf ("  units:         %15" PRId64 "   %10.2f    interval\n", stats.units, relative (stats.conflicts, stats.units));
  printf ("  binaries:      %15" PRId64 "   %10.2f    interval\n", stats.binaries, relative (stats.conflicts, stats.binaries));
  if (all || stats.flush.learned) {
  printf ("flushed:         %15" PRId64 "   %10.2f %%  per conflict\n", stats.flush.learned, percent (stats.flush.learned, stats.conflicts));
  printf ("  hyper:         %15" PRId64 "   %10.2f %%  per conflict\n", stats.flush.hyper, relative (stats.flush.hyper, stats.conflicts));
  printf ("  flushings:     %15" PRId64 "   %10.2f    interval\n", stats.flush.count, relative (stats.conflicts, stats.flush.count));
  }
  if (all || stats.instantiated) {
  printf ("instantiated:    %15" PRId64 "   %10.2f %%  of tried\n", stats.instantiated, percent (stats.instantiated, stats.instried));
  printf ("  instrounds:    %15" PRId64 "   %10.2f %%  of elimrounds\n", stats.instrounds, percent (stats.instrounds, stats.elimrounds));
  }
  if (all || stats.conflicts) {
  printf ("learned:         %15" PRId64 "   %10.2f %%  per conflict\n", stats.learned.clauses, percent (stats.learned.clauses, stats.conflicts));
  printf ("  bumped:        %15" PRId64 "   %10.2f    per learned\n", stats.bumped, relative (stats.bumped, stats.learned.clauses));
  printf ("  recomputed:    %15" PRId64 "   %10.2f %%  per learned\n", stats.recomputed, percent (stats.recomputed, stats.learned.clauses));
  printf ("  promoted1:     %15" PRId64 "   %10.2f %%  per learned\n", stats.promoted1, percent (stats.promoted1, stats.learned.clauses));
  printf ("  promoted2:     %15" PRId64 "   %10.2f %%  per learned\n", stats.promoted2, percent (stats.promoted2, stats.learned.clauses));
  printf ("  improvedglue:  %15" PRId64 "   %10.2f %%  per learned\n", stats.improvedglue, percent (stats.improvedglue, stats.learned.clauses));
  }
  if (all || stats.lucky.succeeded) {
  printf ("lucky:           %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.succeeded, percent (stats.lucky.succeeded, stats.lucky.tried));
  printf ("  constantzero   %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.constant.zero, percent (stats.lucky.constant.zero, stats.lucky.tried));
  printf ("  constantone    %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.constant.one, percent (stats.lucky.constant.one, stats.lucky.tried));
  printf ("  backwardone    %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.backward.one, percent (stats.lucky.backward.one, stats.lucky.tried));
  printf ("  backwardzero   %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.backward.zero, percent (stats.lucky.backward.zero, stats.lucky.tried));
  printf ("  forwardone     %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.forward.one, percent (stats.lucky.forward.one, stats.lucky.tried));
  printf ("  forwardzero    %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.forward.zero, percent (stats.lucky.forward.zero, stats.lucky.tried));
  printf ("  positivehorn   %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.horn.positive, percent (stats.lucky.horn.positive, stats.lucky.tried));
  printf ("  negativehorn   %15" PRId64 "   %10.2f %%  of tried\n", stats.lucky.horn.negative, percent (stats.lucky.horn.negative, stats.lucky.tried));
  }
  printf ("  extendbytes:   %15zd   %10.2f    bytes and MB\n", extendbytes, extendbytes/(double)(1l<<20));
  if (all || stats.learned.clauses)
  printf ("learned_lits:    %15" PRId64 "   %10.2f %%  learned literals\n", stats.learned.literals, percent (stats.learned.literals, stats.learned.literals));
  printf ("minimized:       %15" PRId64 "   %10.2f %%  learned literals\n", stats.minimized, percent (stats.minimized, stats.learned.literals));
  printf ("shrunken:        %15" PRId64 "   %10.2f %%  learned literals\n", stats.shrunken, percent(stats.shrunken, stats.learned.literals));
  printf ("minishrunken:    %15" PRId64 "   %10.2f %%  learned literals\n", stats.minishrunken, percent(stats.minishrunken, stats.learned.literals));

  printf ("propagations:    %15" PRId64 "   %10.2f M  per second\n", propagations, relative (propagations/1e6, t));
  printf ("  coverprops:    %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.cover, percent (stats.propagations.cover, propagations));
  printf ("  probeprops:    %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.probe, percent (stats.propagations.probe, propagations));
  printf ("  searchprops:   %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.search, percent (stats.propagations.search, propagations));
  printf ("  transredprops: %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.transred, percent (stats.propagations.transred, propagations));
  printf ("  vivifyprops:   %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.vivify, percent (stats.propagations.vivify, propagations));
  printf ("  walkprops:     %15" PRId64 "   %10.2f %%  of propagations\n", stats.propagations.walk, percent (stats.propagations.walk, propagations));
  if (all || stats.reactivated) {
  printf ("reactivated:     %15" PRId64 "   %10.2f %%  of all variables\n", stats.reactivated, percent (stats.reactivated, stats.vars));
  }
  if (all || stats.reduced) {
  printf ("reduced:         %15" PRId64 "   %10.2f %%  per conflict\n", stats.reduced, percent (stats.reduced, stats.conflicts));
  printf ("  reductions:    %15" PRId64 "   %10.2f    interval\n", stats.reductions, relative (stats.conflicts, stats.reductions));
  printf ("  collections:   %15" PRId64 "   %10.2f    interval\n", stats.collections, relative (stats.conflicts, stats.collections));
  }
  if (all || stats.rephased.total) {
  printf ("rephased:        %15" PRId64 "   %10.2f    interval\n", stats.rephased.total, relative (stats.conflicts, stats.rephased.total));
  printf ("  rephasedbest:  %15" PRId64 "   %10.2f %%  rephased best\n", stats.rephased.best, percent (stats.rephased.best, stats.rephased.total));
  printf ("  rephasedflip:  %15" PRId64 "   %10.2f %%  rephased flipping\n", stats.rephased.flipped, percent (stats.rephased.flipped, stats.rephased.total));
  printf ("  rephasedinv:   %15" PRId64 "   %10.2f %%  rephased inverted\n", stats.rephased.inverted, percent (stats.rephased.inverted, stats.rephased.total));
  printf ("  rephasedorig:  %15" PRId64 "   %10.2f %%  rephased original\n", stats.rephased.original, percent (stats.rephased.original, stats.rephased.total));
  printf ("  rephasedrand:  %15" PRId64 "   %10.2f %%  rephased random\n", stats.rephased.random, percent (stats.rephased.random, stats.rephased.total));
  printf ("  rephasedwalk:  %15" PRId64 "   %10.2f %%  rephased walk\n", stats.rephased.walk, percent (stats.rephased.walk, stats.rephased.total));
  }
  if (all)
  printf ("rescored:        %15" PRId64 "   %10.2f    interval\n", stats.rescored, relative (stats.conflicts, stats.rescored));
  if (all || stats.restarts) {
  printf ("restarts:        %15" PRId64 "   %10.2f    interval\n", stats.restarts, relative (stats.conflicts, stats.restarts));
  printf ("  reused:        %15" PRId64 "   %10.2f %%  per restart\n", stats.reused, percent (stats.reused, stats.restarts));
  printf ("  reusedlevels:  %15" PRId64 "   %10.2f %%  per restart levels\n", stats.reusedlevels, percent (stats.reusedlevels, stats.restartlevels));
  }
  if (all || stats.restored) {
  printf ("restored:        %15" PRId64 "   %10.2f %%  per weakened\n", stats.restored, percent (stats.restored, stats.weakened));
  printf ("  restorations:  %15" PRId64 "   %10.2f %%  per extension\n", stats.restorations, percent (stats.restorations, stats.extensions));
  printf ("  literals:      %15" PRId64 "   %10.2f    per restored clause\n", stats.restoredlits, relative (stats.restoredlits, stats.restored));
  }
  if (all || stats.stabphases) {
  printf ("stabilizing:     %15" PRId64 "   %10.2f %%  of conflicts\n", stats.stabphases, percent (stats.stabconflicts, stats.conflicts));
  printf ("  restartstab:   %15" PRId64 "   %10.2f %%  of all restarts\n", stats.restartstable, percent (stats.restartstable, stats.restarts));
  printf ("  reusedstab:    %15" PRId64 "   %10.2f %%  per stable restarts\n", stats.reusedstable, percent (stats.reusedstable, stats.restartstable));
  }
  if (all || stats.all.substituted) {
  printf ("substituted:     %15" PRId64 "   %10.2f %%  of all variables\n", stats.all.substituted, percent (stats.all.substituted, stats.vars));
  printf ("  decompositions:%15" PRId64 "   %10.2f    per phase\n", stats.decompositions, relative (stats.decompositions, stats.probingphases));
  }
  if (all || stats.subsumed) {
  printf ("subsumed:        %15" PRId64 "   %10.2f %%  of all clauses\n", stats.subsumed, percent (stats.subsumed, stats.added.total));
  printf ("  subsumephases: %15" PRId64 "   %10.2f    interval\n", stats.subsumephases, relative (stats.conflicts, stats.subsumephases));
  printf ("  subsumerounds: %15" PRId64 "   %10.2f    per phase\n", stats.subsumerounds, relative (stats.subsumerounds, stats.subsumephases));
  printf ("  deduplicated:  %15" PRId64 "   %10.2f %%  per subsumed\n", stats.deduplicated, percent (stats.deduplicated, stats.subsumed));
  printf ("  transreds:     %15" PRId64 "   %10.2f    interval\n", stats.transreds, relative (stats.conflicts, stats.transreds));
  printf ("  transitive:    %15" PRId64 "   %10.2f %%  per subsumed\n", stats.transitive, percent (stats.transitive, stats.subsumed));
  printf ("  subirr:        %15" PRId64 "   %10.2f %%  of subsumed\n", stats.subirr, percent (stats.subirr, stats.subsumed));
  printf ("  subred:        %15" PRId64 "   %10.2f %%  of subsumed\n", stats.subred, percent (stats.subred, stats.subsumed));
  printf ("  subtried:      %15" PRId64 "   %10.2f    tried per subsumed\n", stats.subtried, relative (stats.subtried, stats.subsumed));
  printf ("  subchecks:     %15" PRId64 "   %10.2f    per tried\n", stats.subchecks, relative (stats.subchecks, stats.subtried));
  printf ("  subchecks2:    %15" PRId64 "   %10.2f %%  per subcheck\n", stats.subchecks2, percent (stats.subchecks2, stats.subchecks));
  printf ("  elimotfsub:    %15" PRId64 "   %10.2f %%  of subsumed\n", stats.elimotfsub, percent (stats.elimotfsub, stats.subsumed));
  printf ("  elimbwsub:     %15" PRId64 "   %10.2f %%  of subsumed\n", stats.elimbwsub, percent (stats.elimbwsub, stats.subsumed));
  printf ("  eagersub:      %15" PRId64 "   %10.2f %%  of subsumed\n", stats.eagersub, percent (stats.eagersub, stats.subsumed));
  printf ("  eagertried:    %15" PRId64 "   %10.2f    tried per eagersub\n", stats.eagertried, relative (stats.eagertried, stats.eagersub));
  }
  if (all || stats.strengthened) {
  printf ("strengthened:    %15" PRId64 "   %10.2f %%  of all clauses\n", stats.strengthened, percent (stats.strengthened, stats.added.total));
  printf ("  elimotfstr:    %15" PRId64 "   %10.2f %%  of strengthened\n", stats.elimotfstr, percent (stats.elimotfstr, stats.strengthened));
  printf ("  elimbwstr:     %15" PRId64 "   %10.2f %%  of strengthened\n", stats.elimbwstr, percent (stats.elimbwstr, stats.strengthened));
  }
  if (all || stats.htrs) {
  printf ("ternary:         %15" PRId64 "   %10.2f %%  of resolved\n", stats.htrs, percent (stats.htrs, stats.ternres));
  printf ("  phases:        %15" PRId64 "   %10.2f    interval\n", stats.ternary, relative (stats.conflicts, stats.ternary));
  printf ("  htr3:          %15" PRId64 "   %10.2f %%  ternary hyper ternres\n", stats.htrs3, percent (stats.htrs3, stats.htrs));
  printf ("  htr2:          %15" PRId64 "   %10.2f %%  binary hyper ternres\n", stats.htrs2, percent (stats.htrs2, stats.htrs));
  }
  if (all || vivified) {
  printf ("vivified:        %15" PRId64 "   %10.2f %%  of all clauses\n", vivified, percent (vivified, stats.added.total));
  printf ("  vivifications: %15" PRId64 "   %10.2f    interval\n", stats.vivifications, relative (stats.conflicts, stats.vivifications));
  printf ("  vivifychecks:  %15" PRId64 "   %10.2f %%  per conflict\n", stats.vivifychecks, percent (stats.vivifychecks, stats.conflicts));
  printf ("  vivifysched:   %15" PRId64 "   %10.2f %%  checks per scheduled\n", stats.vivifysched, percent (stats.vivifychecks, stats.vivifysched));
  printf ("  vivifyunits:   %15" PRId64 "   %10.2f %%  per vivify check\n", stats.vivifyunits, percent (stats.vivifyunits, stats.vivifychecks));
  printf ("  vivifysubs:    %15" PRId64 "   %10.2f %%  per subsumed\n", stats.vivifysubs, percent (stats.vivifysubs, stats.subsumed));
  printf ("  vivifystrs:    %15" PRId64 "   %10.2f %%  per strengthened\n", stats.vivifystrs, percent (stats.vivifystrs, stats.strengthened));
  printf ("  vivifystrirr:  %15" PRId64 "   %10.2f %%  per vivifystrs\n", stats.vivifystrirr, percent (stats.vivifystrirr, stats.vivifystrs));
  printf ("  vivifystred1:  %15" PRId64 "   %10.2f %%  per vivifystrs\n", stats.vivifystred1, percent (stats.vivifystred1, stats.vivifystrs));
  printf ("  vivifystred2:  %15" PRId64 "   %10.2f %%  per vivifystrs\n", stats.vivifystred2, percent (stats.vivifystred2, stats.vivifystrs));
  printf ("  vivifystred3:  %15" PRId64 "   %10.2f %%  per vivifystrs\n", stats.vivifystred3, percent (stats.vivifystred3, stats.vivifystrs));
  printf ("  vivifydecs:    %15" PRId64 "   %10.2f    per checks\n", stats.vivifydecs, relative (stats.vivifydecs, stats.vivifychecks));
  printf ("  vivifyreused:  %15" PRId64 "   %10.2f %%  per decision\n", stats.vivifyreused, percent (stats.vivifyreused, stats.vivifydecs));
  }
  if (all || stats.walk.count) {
  printf ("walked:          %15" PRId64 "   %10.2f    interval\n", stats.walk.count, relative (stats.conflicts, stats.walk.count));
#ifndef QUIET
  if (internal->profiles.walk.value > 0)
  printf ("  flips:         %15" PRId64 "   %10.2f M  per second\n", stats.walk.flips, relative (1e-6*stats.walk.flips, internal->profiles.walk.value));
  else
#endif
  printf ("  flips:         %15" PRId64 "   %10.2f    per walk\n", stats.walk.flips, relative (stats.walk.flips, stats.walk.count));
  if (stats.walk.minimum < LONG_MAX)
  printf ("  minimum:       %15" PRId64 "   %10.2f %%  clauses\n", stats.walk.minimum, percent (stats.walk.minimum, stats.added.irredundant));
  printf ("  broken:        %15" PRId64 "   %10.2f    per flip\n", stats.walk.broken, relative (stats.walk.broken, stats.walk.flips));
  }
  if (all || stats.weakened) {
  printf ("weakened:        %15" PRId64 "   %10.2f    average size\n", stats.weakened, relative (stats.weakenedlen, stats.weakened));
  printf ("  extensions:    %15" PRId64 "   %10.2f    interval\n", stats.extensions, relative (stats.conflicts, stats.extensions));
  printf ("  flipped:       %15" PRId64 "   %10.2f    per weakened\n", stats.extended, relative (stats.extended, stats.weakened));
  }

}

void Internal::print_resource_usage () {
  printf ("resources\n");
  uint64_t m = maximum_resident_set_size ();
  printf ("CPUTIME: %12.2f\n", internal->process_time ());
  printf ("WALLCLOCK: %12.2f\n", internal->real_time ());
  printf ("MEM: %12.2f\n", m/(double)(1l<<20));
}

/*------------------------------------------------------------------------*/

void Checker::print_stats () {

  if (!stats.added && !stats.deleted) return;

  printf ("checker statistics\n");

  printf ("checks:          %15" PRId64 "\n", stats.checks);
  printf ("assumptions:     %15" PRId64 "   %10.2f    per check\n", stats.assumptions, relative (stats.assumptions, stats.checks));
  printf ("propagations:    %15" PRId64 "   %10.2f    per check\n", stats.propagations, relative (stats.propagations, stats.checks));
  printf ("original:        %15" PRId64 "   %10.2f %%  of all clauses\n", stats.original, percent (stats.original, stats.added));
  printf ("derived:         %15" PRId64 "   %10.2f %%  of all clauses\n", stats.derived, percent (stats.derived, stats.added));
  printf ("deleted:         %15" PRId64 "   %10.2f %%  of all clauses\n", stats.deleted, percent (stats.deleted, stats.added));
  printf ("insertions:      %15" PRId64 "   %10.2f %%  of all clauses\n", stats.insertions, percent (stats.insertions, stats.added));
  printf ("collections:     %15" PRId64 "   %10.2f    deleted per collection\n", stats.collections, relative (stats.collections, stats.deleted));
  printf ("collisions:      %15" PRId64 "   %10.2f    per search\n", stats.collisions, relative (stats.collisions, stats.searches));
  printf ("searches:        %15" PRId64 "\n", stats.searches);
  printf ("units:           %15" PRId64 "\n", stats.units);
}

}
