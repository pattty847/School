import Vue from 'vue'
import Vuex, { Module, StoreOptions } from 'vuex'
import { registerModule, scheduleSync } from '@/utils/store'

import app, { AppState } from './app'
import settings, { SettingsState } from './settings'
import exchanges, { ExchangesState } from './exchanges'
import panes, { PanesState } from './panes'
import { sleep } from '@/utils/helpers'
import { Workspace } from '@/types/test'
import aggregatorService from '@/services/aggregatorService'

Vue.use(Vuex)

/* console.debug = function() {
  //
} */

export interface AppModuleTree<R> {
  [key: string]: Module<any, R>
}

export interface ModulesState {
  app: AppState
  settings: SettingsState
  panes: PanesState
  exchanges: ExchangesState
}

const store = new Vuex.Store({} as StoreOptions<ModulesState>)
const modules = { app, settings, exchanges, panes } as AppModuleTree<ModulesState>

store.subscribe((mutation, state: any) => {
  const moduleId = mutation.type.split('/')[0]

  // console.debug(`[store] ${mutation.type}`)

  if (state[moduleId] && state[moduleId]._id) {
    scheduleSync(state[moduleId])
  }
})

export async function boot(workspace?: Workspace, previousWorkspaceId?: string) {
  console.log(`[store] booting on workspace "${workspace.name}" (${workspace.id})`)

  if (store.state.app) {
    console.log(`[store] app exists, unload current workspace`)

    store.dispatch('app/setBooted', false)

    console.info(`unloading ${previousWorkspaceId}`)

    await sleep(100)

    const markets = Object.keys(store.state.panes.marketsListeners)

    if (markets.length) {
      // console.info(`disconnect from ` + markets.slice(0, 3).join(', ') + (markets.length - 3 > 0 ? ' + ' + (markets.length - 3) + ' others' : ''))

      await aggregatorService.disconnect(markets)
    }

    for (const id in store.state) {
      console.log(`[store] unloading module ${id}`)
      store.unregisterModule(id)
    }
  }

  console.info(`loading core module`)
  registerModule('app', modules['app'])
  await sleep(10)
  await store.dispatch('app/boot')

  console.info(`setting up workspace`)
  registerModule('settings', modules['settings'])
  await sleep(10)
  await store.dispatch('settings/boot')

  console.info(`loading panes`)
  registerModule('panes', modules['panes'])
  await sleep(10)
  await store.dispatch('panes/boot')

  for (const paneId in store.state.panes.panes) {
    console.info(`registering pane module ${paneId}`)
    await registerModule(paneId, {}, false, store.state.panes.panes[paneId])
  }

  store.dispatch('app/setBooted')

  console.info(`registering exchanges`)
  await registerModule('exchanges', modules['exchanges'])

  for (const paneId in store.state.panes.panes) {
    console.info(`booting module ${paneId}`)

    try {
      await store.dispatch(paneId + '/boot')
    } catch (error) {
      console.error(error)
    }
  }

  console.info(`loading exchanges`)
  await store.dispatch('exchanges/boot')
}

export default store
