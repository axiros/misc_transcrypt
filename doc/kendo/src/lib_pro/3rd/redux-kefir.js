(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('kefir')) :
  typeof define === 'function' && define.amd ? define(['exports', 'kefir'], factory) :
  (factory((global.ReduxKefir = {}),global.Kefir));
}(this, function (exports,kefir) { 'use strict';

  var babelHelpers = {};

  babelHelpers.extends = Object.assign || function (target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i];

      for (var key in source) {
        if (Object.prototype.hasOwnProperty.call(source, key)) {
          target[key] = source[key];
        }
      }
    }

    return target;
  };

  babelHelpers;

  var validKeys = ['type', 'payload', 'error', 'meta'];

  function isValidKey(key) {
    return validKeys.indexOf(key) > -1;
  }

  function isFSA(action) {
    return typeof action === "object" && action !== null && action.constructor === Object && typeof action.type !== "undefined" && Object.keys(action).every(isValidKey);
  }

  function isStore(object) {
    return typeof object === "object" && object !== null && typeof object.subscribe === "function" && typeof object.getState === "function";
  }

  function isObservable(object) {
    return object instanceof kefir.Observable;
  }

  function observableMiddleware(_ref) {
    var dispatch = _ref.dispatch;

    return function (next) {
      return function (action) {
        if (!isFSA(action)) {
          return isObservable(action) ? action.onValue(dispatch) : next(action);
        }

        if (isObservable(action.payload)) {
          return action.payload.onValue(function (value) {
            dispatch(babelHelpers.extends({}, action, { payload: value }));
          }).onError(function (error) {
            dispatch(babelHelpers.extends({}, action, { payload: error, error: true }));
          });
        }

        return next(action);
      };
    };
  }

  function createProjection(store) {
    if (!isStore(store)) throw new TypeError("createProjection: store expected");

    function onActivation(emitter) {
      return store.subscribe(function () {
        return emitter.emit(store.getState());
      });
    }

    return kefir.stream(onActivation).toProperty(store.getState);
  }

  exports.observableMiddleware = observableMiddleware;
  exports.createProjection = createProjection;

}));

