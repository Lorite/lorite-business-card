(function () {
  const SC = (window.SCENES = window.SCENES || {});
  const R = window.RIG;
  SC['card-duo'] = {
    dur: 4, width: 240, loopOnly: true, label: 'Spot tracks the drone with its arm camera.',
    draw(g, S) {
      const Q = R.quad(g, -45, { sx: 1, armK: 1, aim: [44, -88], reachD: 40, t: 0 });
      R.sightCone(g, Q.cam, [52, -96], 1, 0, { w: 7, dots: 0 });
      R.drone(g, 52, -96, { s: 2.2, guards: true, tilt: 0.08, t: 0 });
    },
  };
})();
